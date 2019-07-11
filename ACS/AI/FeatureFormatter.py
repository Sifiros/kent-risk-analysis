#!/usr/local/bin/python3

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
            'doNotTrack' : self.doNotTrack_formater
        }

        self.m_formated_data = {}

    def format(self):
        for key in self.m_data:
            self.m_treatment_units[key](self.m_data[key])
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
        self.m_formated_data['do_not_track'] = data # e.g. : true

    def plugins_formater(self, data):
        pass

    def uaInfo_formater(self, data):
        pass

    def acceptedCharset_formater(self, data):
        pass

    def acceptedEncoding_formater(self, data):
        pass

    def acceptedMime_formater(self, data):
        pass

    def acceptedLanguage_formater(self, data):
        pass

if __name__ == "__main__":
    pass