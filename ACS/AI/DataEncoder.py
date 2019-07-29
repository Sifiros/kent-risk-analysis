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
    
class FeatureFormater():
    
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

        self.m_formated_data = {}
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
        try:
            for key in self.m_data:
                self.m_treatment_units[key](self.m_data[key])
        except KeyError:
            print('ERROR : Invalid JSON input (invalid key)')
            exit(1)

        self.save_table_update_on_redis()

        print(self.m_formated_data)

    def colorDepth_formater(self, data):
        self.m_formated_data['color_depth'] = data # e.g. : 16 

    def innerSize_formater(self, data):
        data.split(':')
        self.m_formated_data['inner_size'] = { # e.g. : { width : 1920,  height : 1080 } 
            'width' : data[0],
            'height' : data[1]
        }

    def outerSize_formater(self, data):
        data.split(':')
        self.m_formated_data['outer_size'] = { # e.g. : { width : 1920,  height : 1080 } 
            'width' : data[0],
            'height' : data[1]
        }

    def screenSize_formater(self, data):
        data.split(':')
        self.m_formated_data['screen_size'] = { # e.g. : { width : 1920,  height : 1080 } 
            'width' : data[0],
            'height' : data[1]
        }

    def timezoneOffset_formater(self, data):
        self.m_formated_data['timezone_offset'] = data # e.g. : -120

    def position_formater(self, data):
        self.m_formated_data['position'] = data # e.g. : { latitude : 12342.322, longitude  : 112342.3432 }

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
        self.m_formated_data['plugins'] = formated_plugins_list

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
                    formated_ua[key] = -1 if self.is_engine_empty(data[key]) else self.component_formater(data[key], table)
                elif key == "ua":
                    formated_ua[key] = self.ua_formater(data[key])
                else:
                    formated_ua[key] = self.component_formater(data[key], table)
            except KeyError:
                formated_ua[key] = -1 # Key undefined in the current subset of data
        self.m_formated_data['uaInfo'] = formated_ua

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
        self.m_formated_data['acceptedCharset'] = self.special_component_formater(data, self.m_accepted_charset_table)

    def acceptedEncoding_formater(self, data):
        self.m_formated_data['acceptedEncoding'] = self.special_component_formater(data, self.m_accepted_encoding_table)

    def acceptedMime_formater(self, data):
        self.m_formated_data['acceptedMime'] = self.special_component_formater(data, self.m_accepted_mime_table)

    def acceptedLanguage_formater(self, data):
        self.m_formated_data['acceptedLanguage'] = self.special_component_formater(data, self.m_accepted_languages_table)

    def canvas_formater(self,  data):
        self.m_formated_data['canvas'] = self.special_component_formater(data, self.m_canvas_table)

def open_json(path):
    with open(path) as json_file:  
        data = json.load(json_file)
        return data

def main(json_path):
    data = open_json(json_path)
    FeatureFormater(data["-LiHvLhPIkMKO9lWTcPX"])

if __name__ == "__main__":
    plac.call(main)