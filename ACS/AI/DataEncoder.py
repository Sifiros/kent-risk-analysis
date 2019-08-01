#!/usr/local/bin/python3
import redis
import json
import plac
import re

class RedisStore():

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def get_transformation_table(self, table_name):
        key = "transTable/{}".format(table_name)
        content = self.redis.get(key)
        if content is None:
            return {}
        else:
            return json.loads(content)

    def set_transformation_table(self, table_name, table):
        key = "transTable/{}".format(table_name)
        self.redis.set(key, json.dumps(table))

redisStore = RedisStore()

class TransTableUtils():

    @staticmethod
    def get_browser_table_model():
        return {
            "appName": None,
            "major": None,
            "name": None,
            "version": None
        }

    @staticmethod
    def get_engine_table_model():
        return {
            "name": None,
            "version": None
        } 

    @staticmethod
    def get_os_table_model():
        return {
            "name": None,
            "version": None
        }
    
    @staticmethod
    def get_cpu_table_model():
        return {
            "architecture": None
        }

    @staticmethod
    def get_device_table_model():
        return {
            "model": None,
            "type": None,
            "vendor": None
        }
    
class DataEncoder():
    
    def __init__(self, data):
        self.m_data = data

        self.m_treatment_units = {
            'colorDepth' : self.colorDepth_formater,
            'innerSize' : self.innerSize_formater,
            'outerSize' : self.outerSize_formater,
            'screenSize' : self.screenSize_formater,
            'timezoneOffset' : self.timezoneOffset_formater,
            'plugins' : self.plugins_formater,
            'position' : self.position_formater,
            'uaInfo' : self.uaInfo_formater,
            'acceptedCharset' : self.acceptedCharset_formater,
            'acceptedEncoding' : self.acceptedEncoding_formater,
            'acceptedMime' : self.acceptedMime_formater,
            'acceptedLanguages' : self.acceptedLanguage_formater,
            'doNotTrack' : self.doNotTrack_formater,
            'canvas' : self.canvas_formater
        }

        self.m_formated_data = {
            "browser_id": data["browser_id"]
        }
        self.m_browser_table = TransTableUtils.get_browser_table_model()
        self.m_engine_table = TransTableUtils.get_engine_table_model()
        self.m_os_table = TransTableUtils.get_os_table_model()
        self.m_cpu_table = TransTableUtils.get_cpu_table_model()
        self.m_device_table = TransTableUtils.get_device_table_model()

        try:
            self.recover_special_table()
            self.recover_table(self.m_browser_table, 'browserTable')
            self.recover_table(self.m_engine_table, 'engineTable')
            self.recover_table(self.m_os_table, 'osTable')
            self.recover_table(self.m_cpu_table, 'cpuTable')
            self.recover_table(self.m_device_table, 'deviceTable')
        except redis.exceptions.ConnectionError:
            print('ERROR : Connection with redis DB refused')
            exit(1)

        self.format()


    def recover_table(self, table, table_name):
        for key, data in table.items():
            table[key] = redisStore.get_transformation_table('{}/{}'.format(table_name, key))
    
    def recover_special_table(self):
        self.m_plugins_table = redisStore.get_transformation_table('pluginsTable')
        self.m_ua_table = redisStore.get_transformation_table('uaTable')
        self.m_accepted_charset_table = redisStore.get_transformation_table('acceptedCharsetTable')
        self.m_accepted_encoding_table = redisStore.get_transformation_table('acceptedEncodingTable')
        self.m_accepted_mime_table = redisStore.get_transformation_table('acceptedMimeTable')
        self.m_accepted_languages_table = redisStore.get_transformation_table('acceptedLanguagesTable')
        self.m_canvas_table = redisStore.get_transformation_table('canvasTable')

    def save_table(self, table, table_name):
        for key, data in table.items():
            redisStore.set_transformation_table('{}/{}'.format(table_name, key), table[key])

    def save_special_table(self):
        redisStore.set_transformation_table('pluginsTable', self.m_plugins_table)
        redisStore.set_transformation_table('uaTable', self.m_ua_table)
        redisStore.set_transformation_table('acceptedCharsetTable', self.m_accepted_charset_table)
        redisStore.set_transformation_table('acceptedEncodingTable', self.m_accepted_encoding_table)
        redisStore.set_transformation_table('acceptedMimeTable', self.m_accepted_mime_table)
        redisStore.set_transformation_table('acceptedLanguagesTable', self.m_accepted_languages_table)
        redisStore.set_transformation_table('canvasTable', self.m_canvas_table)

    def save_table_update_on_redis(self):
        self.save_special_table()
        self.save_table(self.m_browser_table, 'browserTable')
        self.save_table(self.m_engine_table, 'engineTable')
        self.save_table(self.m_os_table, 'osTable')
        self.save_table(self.m_cpu_table, 'cpuTable')
        self.save_table(self.m_device_table, 'deviceTable')

    # Perform a OHV (One Hot Vector) encoding on each Json keys
    def format(self):
        for key in self.m_data:
            try:
                self.m_treatment_units[key](self.m_data[key])
            except KeyError:
                pass

        self.save_table_update_on_redis()

        # print(json.dumps(self.m_formated_data))

    def colorDepth_formater(self, data):
        self.m_formated_data['color_depth'] = data # e.g. : 16 

    def innerSize_formater(self, data):
        data.split(':')
        self.m_formated_data['inner_size_width'] = int(data[0])
        self.m_formated_data['inner_size_height'] = int(data[1])

    def outerSize_formater(self, data):
        data.split(':')
        self.m_formated_data['outer_size_width'] = int(data[0])
        self.m_formated_data['outer_size_height'] = int(data[1])

    def screenSize_formater(self, data):
        data.split(':')
        self.m_formated_data['screen_size_width'] = int(data[0])
        self.m_formated_data['screen_size_height'] = int(data[1])

    def timezoneOffset_formater(self, data):
        self.m_formated_data['timezone_offset'] = data # e.g. : -120

    def position_formater(self, data):
        self.m_formated_data['position_latitude'] = data['latitude']
        self.m_formated_data['position_longitude'] = data['longitude']

    def doNotTrack_formater(self, data):
        self.m_formated_data['do_not_track'] = data # e.g. : True

    def plugins_formater(self, data): # e.g. : {[1, 2, 3]}
        formated_plugins_list = []
        for plugin in data:
            if plugin in self.m_plugins_table:
                formated_plugins_list.append(self.m_plugins_table[plugin])
            else:
                self.m_plugins_table[plugin] = len(self.m_plugins_table) + 1
                formated_plugins_list.append(self.m_plugins_table[plugin])

        i = 0
        for entry in formated_plugins_list:
            self.m_formated_data['plugins_{}'.format(i)] = entry
            i += 1
        while i < 15: # Pad for data consistency
            self.m_formated_data['plugins_{}'.format(i)] = -1
            i += 1

    def uaInfo_formater(self, data):
        formated_ua = {}
        
        table_dic = {
            "browser" : self.m_browser_table,
            "engine" : self.m_engine_table,
            "os" : self.m_os_table,
            "cpu" : self.m_cpu_table,
            "device" : self.m_device_table,
            "ua" : self.m_ua_table
        }

        for key, table in table_dic.items():
            try:
                if key == "engine":
                    if not self.is_engine_empty(data[key]):
                        formated_ua[key] = self.component_formater(data[key], table)
                elif key == "ua":
                    value = self.ua_formater(data[key])
                    if value != -1:
                        formated_ua[key] = value
                else:
                    value = self.component_formater(data[key], table)
                    if value != -1:
                        formated_ua[key] = value
            except KeyError:
                pass

        for key, entry in formated_ua.items():
            if type(entry) is not dict:
                self.m_formated_data['uaInfo_{}'.format(key)] = entry
            else:
                for subkey, subentry in entry.items():
                    self.m_formated_data['uaInfo_{}_{}'.format(key, subkey)] = subentry

    def is_engine_empty(self, data):
        if data['name'] == "Blink": # Engine is undefined in the subset, abort formating
            return True
        return False

    def component_formater(self, data, table):
        formated_component = {}
        for key, component_data in data.items():
            if component_data in table[key]:
                formated_component.update({key : table[key][component_data]})
            else:
                table[key].update({component_data : len(table[key]) + 1})
                formated_component.update({key : table[key][component_data]})
        return formated_component

    def special_component_formater(self, data, table):
        formated_data = -1
        table_cpy = table.copy()
        if len(table_cpy) == 0:
            table.update({data : len(table) + 1})
            formated_data = table[data]
        else:
            is_new = True
            for entry in table_cpy:
                if data == entry:
                    formated_data = table[data]
                    is_new = False
                    break
            if is_new:
                table.update({data : len(table) + 1})
                formated_data = table[data]
        return formated_data

    def ua_formater(self, data):
        return self.special_component_formater(data, self.m_ua_table)

    def acceptedCharset_formater(self, data):
        value = self.special_component_formater(data, self.m_accepted_charset_table)
        if value != -1:
            self.m_formated_data['acceptedCharset'] = value

    def acceptedEncoding_formater(self, data):
        value = self.special_component_formater(data, self.m_accepted_encoding_table)
        if value != -1:
            self.m_formated_data['acceptedEncoding'] = value

    def acceptedMime_formater(self, data):
        value = self.special_component_formater(data, self.m_accepted_mime_table)
        if value != -1:
            self.m_formated_data['acceptedMime'] = value        

    def acceptedLanguage_formater(self, data):
        value = self.special_component_formater(data, self.m_accepted_languages_table)
        if value != -1:
            self.m_formated_data['acceptedLanguage'] = value

    def canvas_formater(self,  data):
        value = self.special_component_formater(data, self.m_canvas_table)
        if value != -1:
            self.m_formated_data['canvas'] = value

def open_json(path):
    with open(path) as json_file:  
        data = json.load(json_file)
        return data

def main(json_path):
    data = open_json(json_path)
    DataEncoder(data["-LiHvLhPIkMKO9lWTcPX"])

if __name__ == "__main__":
    plac.call(main)
