#!/usr/local/bin/python3
import redis
import json
import plac
import re
from config import REDIS_HOST, REDIS_PORT

# Helper class used to communicate with Redis API 
class RedisStore():

    def __init__(self):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

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

# Helper used to get the different models used into user's profile
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

# Allow to perform a One Hot Vector on user's profile
# to allow its usablity by the AI 
class DataEncoder():
    
    # Take an user's profil in input.
    # Init the class's factory (m_treatment_units), recover the different tables from Redis DB and then launch encoding.
    def __init__(self, data):
        self.m_data = data

        self.m_treatment_units = {
            'colorDepth' : self.colorDepth_formater,
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

    # Perform a OHV (One Hot Vector) encoding on each Json keys
    def format(self):
        for key in self.m_treatment_units:
            if key in self.m_data:
                self.m_treatment_units[key](self.m_data[key])
            else:
                self.m_treatment_units[key]()

        self.save_table_update_on_redis()

    # Allow to recover a generic table from Redis DB according to its name 
    def recover_table(self, table, table_name):
        for key, data in table.items():
            table[key] = redisStore.get_transformation_table('{}/{}'.format(table_name, key))
    
    # Recover all the special formated tables from Redis DB
    def recover_special_table(self):
        self.m_screen_size_table = redisStore.get_transformation_table('screenSizeTable')
        self.m_inner_size_table = redisStore.get_transformation_table('innerSizeTable')
        self.m_outer_size_table = redisStore.get_transformation_table('outerSizeTable')
        self.m_plugins_table = redisStore.get_transformation_table('pluginsTable')
        self.m_ua_table = redisStore.get_transformation_table('uaTable')
        self.m_accepted_charset_table = redisStore.get_transformation_table('acceptedCharsetTable')
        self.m_accepted_encoding_table = redisStore.get_transformation_table('acceptedEncodingTable')
        self.m_accepted_mime_table = redisStore.get_transformation_table('acceptedMimeTable')
        self.m_accepted_languages_table = redisStore.get_transformation_table('acceptedLanguagesTable')
        self.m_canvas_table = redisStore.get_transformation_table('canvasTable')

    # Allow to save a generic table to Redis DB according to its name
    def save_table(self, table, table_name):
        for key, data in table.items():
            redisStore.set_transformation_table('{}/{}'.format(table_name, key), table[key])

    # Save all the special formated tables to Redis DB
    def save_special_table(self):
        redisStore.set_transformation_table('screenSizeTable', self.m_screen_size_table)
        redisStore.set_transformation_table('innerSizeTable', self.m_inner_size_table)
        redisStore.set_transformation_table('outerSizeTable', self.m_outer_size_table)
        redisStore.set_transformation_table('pluginsTable', self.m_plugins_table)
        redisStore.set_transformation_table('uaTable', self.m_ua_table)
        redisStore.set_transformation_table('acceptedCharsetTable', self.m_accepted_charset_table)
        redisStore.set_transformation_table('acceptedEncodingTable', self.m_accepted_encoding_table)
        redisStore.set_transformation_table('acceptedMimeTable', self.m_accepted_mime_table)
        redisStore.set_transformation_table('acceptedLanguagesTable', self.m_accepted_languages_table)
        redisStore.set_transformation_table('canvasTable', self.m_canvas_table)

    # Save all the tables to Redis DB
    def save_table_update_on_redis(self):
        self.save_special_table()
        self.save_table(self.m_browser_table, 'browserTable')
        self.save_table(self.m_engine_table, 'engineTable')
        self.save_table(self.m_os_table, 'osTable')
        self.save_table(self.m_cpu_table, 'cpuTable')
        self.save_table(self.m_device_table, 'deviceTable')

    # Format color depth field
    # e.g : in => 16| out => 16
    def colorDepth_formater(self, data=-1):
        self.m_formated_data['color_depth'] = data

    # Format screen size field
    # e.g : in => "1920:1080" | out => 1
    def screenSize_formater(self, data=None):
        self.m_formated_data['screen_size'] = self.special_component_formater(data, self.m_screen_size_table)

    # Format timezone offset field
    # e.g : in => -120 | out => -120
    def timezoneOffset_formater(self, data=-1):
        self.m_formated_data['timezone_offset'] = data

    # Format position_latitude and position_longitude fields
    # e.g : in => {"position":{"latitude": 1.1234565, "longitude": 34.2345}} | out => {"position_latitude":1.1234565, "position_longitude":34.2345}
    def position_formater(self, data=None):
        try:
            latitude = data['latitude']
            longitude = data['longitude']
        except:
            latitude = -1
            longitude = -1
        self.m_formated_data['position_latitude'] = latitude
        self.m_formated_data['position_longitude'] = longitude

    # Format do not track field
    # e.g : in => 0 | out => 0
    def doNotTrack_formater(self, data=-1):
        self.m_formated_data['do_not_track'] = data

    # Format plugins field
    # e.g : in => {"plugins": ["chrome", "netflix"]} | out => {"plugin_0": 1, "plugin_1": 2, "plugin_2": 0, "plugin_3": 0, ..., "plugin_15": 0}
    def plugins_formater(self, data=[]):
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
        while i < 12: # Pad for data consistency with Random Forest
            self.m_formated_data['plugins_{}'.format(i)] = -1
            i += 1

    # Format uaInfo fields
    # e.g : in => {"uaInfo": {"browser": {'appName': 'Netscape', 'major': '67', 'name': 'Firefox', 'version': '67.0'}, ..., "os" : {'name': 'Windows', 'version': '10'}}} | out => {"ua_info_browser_appName": 0, "ua_info_browser_major": 68, ..., "ua_info_os_version": 10}
    def uaInfo_formater(self, data={}):
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
                    value = {"name": -1, "version": -1} if key not in data or data[key]['name'] == 'Blink' else self.component_formater(data[key], table)
                    formated_ua[key] = value
                elif key == "ua":
                    value = self.ua_formater(data[key]) if key in data else -1
                    formated_ua[key] = value
                else:
                    formated_ua[key] = self.component_formater(data[key], table)
                    # Fix missing values 
                    default_values = {
                        'device': {'model': -1, 'type': -1, 'vendor': -1},
                        'cpu': {'architecture': -1},
                        'os': {'name': -1, 'version': -1}
                    }[key]
                    for subkey in default_values.keys():
                        if subkey not in formated_ua[key]:
                            formated_ua[key][subkey] = default_values[subkey]
            except KeyError:
                pass

        for key, entry in formated_ua.items():
            if type(entry) is not dict:
                self.m_formated_data['uaInfo_{}'.format(key)] = entry
            else:
                for subkey, subentry in entry.items():
                    self.m_formated_data['uaInfo_{}_{}'.format(key, subkey)] = subentry

    # Format a generic component by performing a One Hot Vector on it thanks to the values stored on Redis DB
    def component_formater(self, data, table):
        formated_component = {}
        for key, component_data in data.items():
            if component_data in table[key]:
                formated_component.update({key : table[key][component_data]})
            else:
                table[key].update({component_data : len(table[key]) + 1})
                formated_component.update({key : table[key][component_data]})
        return formated_component

    # Format a special formated component by performing a One Hot Vector on it thanks to the values stored on Redis DB
    def special_component_formater(self, data, table):
        if data is None:
            return -1
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

    # Format ua field
    # e.g : in => {"ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0"} | out => {"ua_info_ua": 0}
    def ua_formater(self, data):
        return self.special_component_formater(data, self.m_ua_table)

    # Format accepted charset field
    # e.g : in => {"acceptedCharset": "utf-8, iso-8859-1;q=0.5"} | out => {"acceptedCharset": 0}
    def acceptedCharset_formater(self, data=None):
        value = self.special_component_formater(data, self.m_accepted_charset_table)
        self.m_formated_data['acceptedCharset'] = value

    # Format accepted encoding field
    # e.g : in =>  {"acceptedEncoding": "gzip, deflate"} | out => {"acceptedEncoding": 0}
    def acceptedEncoding_formater(self, data=None):
        value = self.special_component_formater(data, self.m_accepted_encoding_table)
        self.m_formated_data['acceptedEncoding'] = value

    # Format accepted mime field
    # e.g : in =>  {"acceptedMime": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"} | out => {"acceptedMime": 0}
    def acceptedMime_formater(self, data=None):
        value = self.special_component_formater(data, self.m_accepted_mime_table)
        self.m_formated_data['acceptedMime'] = value        

    # Format accepted language field
    # e.g : in =>  {"acceptedLanguage": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"} | out => {"acceptedLanguage": 0}
    def acceptedLanguage_formater(self, data=None):
        value = self.special_component_formater(data, self.m_accepted_languages_table)
        self.m_formated_data['acceptedLanguage'] = value

    # Format canvas field
    # e.g : in =>  {"canvas": "U0m1LbbnF/ApP8GoJLFYm125lR164aNff169Hj/rO6CJb4xfjeiVbfOqgllyx7pvmFDH9..."} | out => {"canvas": 0}
    def canvas_formater(self,  data=None):
        value = self.special_component_formater(data, self.m_canvas_table)
        self.m_formated_data['canvas'] = value