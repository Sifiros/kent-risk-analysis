#!/usr/local/bin/python3
import redis
import json
import plac

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
            'acceptedLanguage' : self.acceptedLanguage_formater,
            'doNotTrack' : self.doNotTrack_formater,
            'canvas' : self.canvas_formater
        }

        self.m_formated_data = {}

        self.recover_plugin_table()
        self.recover_browser_table()
        self.recover_engine_table()
        self.recover_os_table()
        self.recover_cpu_table()
        self.recover_device_table()

        self.format()


    def recover_plugin_table(self):
        self.m_plugins_table = redisStore.get_transformation_table('pluginsTable')

    def recover_browser_table(self):
        self.m_browser_table = {}

        self.m_browser_table['appName'] = redisStore.get_transformation_table('browserTable/appName')
        self.m_browser_table['major'] = redisStore.get_transformation_table('browserTable/major')
        self.m_browser_table['name'] = redisStore.get_transformation_table('browserTable/name')
        self.m_browser_table['version'] = redisStore.get_transformation_table('browserTable/version')

    def recover_engine_table(self):
        self.m_engine_table = {}

        self.m_engine_table['name'] = redisStore.get_transformation_table('engineTable/name')
        self.m_engine_table['version'] = redisStore.get_transformation_table('engineTable/version')

    def recover_os_table(self):
        self.m_os_table = {}

        self.m_os_table['name'] = redisStore.get_transformation_table('osTable/name')
        self.m_os_table['version'] = redisStore.get_transformation_table('osTable/version')

    def recover_cpu_table(self):
        self.m_cpu_table = {}

        self.m_cpu_table['architecture'] = redisStore.get_transformation_table('cpuTable/architecture')

    def recover_device_table(self):
        self.m_device_table = {}

        self.m_device_table['model'] = redisStore.get_transformation_table('deviceTable/model')
        self.m_device_table['type'] = redisStore.get_transformation_table('deviceTable/type')
        self.m_device_table['vendor'] = redisStore.get_transformation_table('deviceTable/vendor')

    def save_table_update_on_redis(self):
        redisStore.set_transformation_table('pluginsTable', self.m_plugins_table)

        redisStore.set_transformation_table('browserTable/appName', self.m_browser_table['appName'])
        redisStore.set_transformation_table('browserTable/major', self.m_browser_table['major'])
        redisStore.set_transformation_table('browserTable/name', self.m_browser_table['name'])
        redisStore.set_transformation_table('browserTable/version', self.m_browser_table['version'])

        redisStore.set_transformation_table('engineTable/name', self.m_engine_table['name'])
        redisStore.set_transformation_table('engineTable/version', self.m_engine_table['version'])

        redisStore.set_transformation_table('osTable/name', self.m_os_table['name'])
        redisStore.set_transformation_table('osTable/version', self.m_os_table['version'])

        redisStore.set_transformation_table('cpuTable/architecture', self.m_cpu_table['architecture'])

        redisStore.set_transformation_table('deviceTable/model', self.m_device_table['model'])
        redisStore.set_transformation_table('deviceTable/type', self.m_device_table['type'])
        redisStore.set_transformation_table('deviceTable/vendor', self.m_device_table['vendor'])

    def format(self):
        for key in self.m_data:
            self.m_treatment_units[key](self.m_data[key])

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
            "device" : self.m_device_table
        }

        for key, table in table_dic.items():
            try:
                if key == "engine":
                    formated_ua[key] = self.engine_formater(data[key], table)
                else:
                    formated_ua[key] = self.component_formater(data[key], table)
            except KeyError:
                formated_ua[key] = -1 # Key undefined in the current subset of data

        self.m_formated_data['uaInfo'] = formated_ua

    def engine_formater(self, data, table): 
        formated_engine = {}
        if data['name'] == "Blink": # Engine is undefined in the subset, abort formating
            return -1

        return self.component_formater(data, self.m_engine_table)

    def component_formater(self, data, table):
        formated_component = {}
        for key, component_data in data.items():
            if component_data in table[key]:
                formated_component.update({key : table[key][component_data]})
            else:
                table[key].update({component_data : len(table[key]) + 1})
                formated_component.update({key : table[key][component_data]})
        return formated_component

    def acceptedCharset_formater(self, data):
        pass

    def acceptedEncoding_formater(self, data):
        pass

    def acceptedMime_formater(self, data):
        pass

    def acceptedLanguage_formater(self, data):
        pass

    def canvas_formater(self,  data):
        pass

def open_json(path):
    with open(path) as json_file:  
        data = json.load(json_file)
        return data

def main(json_path):
    data = open_json(json_path)
    FeatureFormater(data["-LiHvLhPIkMKO9lWTcPX"])

if __name__ == "__main__":
    plac.call(main)