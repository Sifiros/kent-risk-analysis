#!/usr/local/bin/python3

import random
import math
import json
import uuid
import copy
import itertools
import difflib
import plac
from DataEncoder import DataEncoder

class FeatureMeta(type):
    def __new__(cls, name, bases, attrs):
        method_list = [
            "check_for_updates", "random_update", "initial_value",
            "find_profile_update_rate", "set_next_update_day",
            "update", "slight_update"
        ]

        base_methods = {
            name: getattr(cls, name) for name in method_list
        }
        base_methods.update(attrs)

        def __init__(self, singularity_ratio):
            self.singularity_ratio = singularity_ratio
            self.value = None
            self.initial_value()
            if hasattr(self, "population_update_rates"):
                self.population_update_rates.sort(
                    key=lambda percentage: percentage[0], # Index 0 is percentage of population
                    reverse=True
                )
                # Select right population"s frequency in which given profile falls
                self.update_rate = self.find_profile_update_rate()
                self.last_update_day = 0
                self.set_next_update_day()

        base_methods["__init__"] = __init__

        return super(FeatureMeta, cls).__new__(cls, name, bases, base_methods)

    def set_next_update_day(self):
        if self.update_rate == NEVER:
            self.next_update_day = NEVER
            return
        # Random value keeping randomness around desired rate, between -rate/2 & +rate/2
        uncertainty = (random.random() * self.update_rate) - (self.update_rate / 2)
        # Finally set next update day
        self.next_update_day = self.last_update_day + self.update_rate + uncertainty        

    def find_profile_update_rate(self):
        ratioSum = 0
        for ratio in self.population_update_rates:
            ratioSum += ratio[0]
            if ratioSum >= self.singularity_ratio: # given profile originality fall in this category
                return ratio[1]
        raise Exception("Feature update rates do not sum up to 1")

    def check_for_updates(self, day):
        if not hasattr(self, "population_update_rates"):
            raise Exception("Missing updates frequency for daily update")
        if day < self.next_update_day:
            return False
        try:
            self.update()
        except: # Currently impossible to update, cancel
            return False
        self.last_update_day = day
        self.set_next_update_day()
        return True

    def update(self):
        self.value = self.random_update()

    def initial_value(self):
        self.value = self.random_update()

    # Update methods
    def random_update(self):
        index = random.randint(1, len(self.possible_values)) - 1
        return copy.copy(self.possible_values[index])

    def slight_update(self):
        ratio = 0
        new_value = ""
        while ratio < 0.75:
            new_value = self.random_update()
            ratio = difflib.SequenceMatcher(None, self.value, new_value).ratio()
        return new_value

NEVER = 100000000 # For pseudo-NEVER Rates

class AcceptedCharsetFeature(metaclass=FeatureMeta):
    possible_values = [
        "utf-8, iso-8859-1;q=0.5",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    ]

class AcceptedEncodingFeature(metaclass=FeatureMeta): # random updates
    possible_values = [
        "gzip, deflate"
    ]
    
    population_update_rates = [
        (0.5, NEVER), (0.35, NEVER), (0.1, 106), (0.05, 60)
    ]    

class AcceptedLanguagesFeature(metaclass=FeatureMeta): # Random updates keeping a 0.75 similarity ratio
    possible_values = [
        "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
    ]
    
    population_update_rates = [
        (0.5, NEVER), (0.35, NEVER), (0.1, 215), (0.05, 58)
    ]

    def update(self):
        self.value = self.slight_update()

class AcceptedMimeFeature(metaclass=FeatureMeta): # Random updates keeping a 0.75 similarity ratio
    possible_values = [
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ]

    population_update_rates = [
        (0.5, NEVER), (0.35, NEVER), (0.1, 164), (0.05, 109)
    ]
    
    def update(self):
        self.value = self.slight_update()    

class DoNotTrackFeature(metaclass=FeatureMeta):
    possible_values = [
        1, 0
    ]

class ScreenSizeFeature(metaclass=FeatureMeta): # random updates
    possible_values = [
        "1920:1080",
        "375:812",
        "1680:1050",
        "1440:900",
        "360:640",
        "600:960",
        "1536:864",
        "1280:720",
        "1366:768",
        "412:732"
    ]
        
    population_update_rates = [
        (0.5, 20), (0.35, 20), (0.1, 3), (0.05, 2)
    ]

class InnerSizeFeature(metaclass=FeatureMeta):
    possible_values = [
        "1680:931",
        "375:635",
        "1920:937",
        "1920:1005",
        "1680:916",
        "1366:608",
        "1280:603",
        "1030:837",
        "360:526",
        "412:652"
    ]

    population_update_rates = [
        (0.5, 3), (0.35, 3), (0.1, 3), (0.05, 2)
    ]

class OuterSizeFeature(metaclass=FeatureMeta):
    possible_values = [
        "1680:1027",
        "375:812",
        "1920:1040",
        "1936:1096",
        "1680:979",
        "1030:900",
        "360:526",
        "1912:1020",
        "600:935",
        "360:526"
    ]

    population_update_rates = [
        (0.5, 3), (0.35, 3), (0.1, 3), (0.05, 2)
    ]

class PluginsFeature(metaclass=FeatureMeta): # updates append or remove a plugin
    possible_values = [
        "Adblocks",
        "reading-list",
        "url-render",
        "google-translate",
        "evernote",
        "cors-everywhere",
        "google-scholar",
        "wordreference"
    ]

    population_update_rates = [
        (0.5, 44), (0.35, 28), (0.1, 12), (0.05, 9)
    ]

    def update(self):
        r = random.random()
        append_probability_threshold = math.exp(len(self.value) / self.max_plugins) / math.exp(1)
        if r >= append_probability_threshold: # add a plugin
            available_plugins = set(self.possible_values) - set(self.value)
            r = random.randint(1, len(available_plugins)) - 1
            self.value.append(list(available_plugins)[r])
        else: # remove one
            r = random.randint(1, len(self.value)) - 1
            self.value.pop(r)

    def initial_value(self):
        # Depending on profile originality, define a max nb plugins value
        if (0 <= self.singularity_ratio <= 0.3):
            self.max_plugins = 0
        elif (0.3 <= self.singularity_ratio <= 0.6):
            self.max_plugins = 3
        elif (0.6 <= self.singularity_ratio <= 0.8):
            self.max_plugins = 6
        else:
            self.max_plugins = 15

        available_plugins = [*self.possible_values]
        random.shuffle(available_plugins)
        desired_nb_plugins = random.randint(0, min(len(self.possible_values), self.max_plugins))
        self.value = self.possible_values[0:desired_nb_plugins]
        
class TimezoneOffsetFeature(metaclass=FeatureMeta): # random updates
    possible_values = [600, 540, 480, 420, 360, 300, 240, 180, 120, 60, 0, -60, -120, -180, -240, -300, -360, -420, -480, -540, -600]
    population_update_rates = [
        (0.5, 206), (0.35, 150), (0.1, 54), (0.05, 27)
    ]    

class BrowserFeature(metaclass=FeatureMeta):  # updates increase version or leave it constant
    possible_values = [
        {"appName": "Netscape", "major": "67", "name": "Firefox", "version": "67.0"},
        {"appName": "Netscape", "major": "220", "name": "Mobile Safari", "version": "220.0.0.20.121"},
        {"appName": "Netscape", "major": "75", "name": "Chrome", "version": "75.0.3770.100"},
        {"appName": "Netscape", "major": "12", "name": "Safari", "version": "12.1.1"},
        {"appName": "Netscape", "major": "17", "name": "Edge", "version": "17.17134"},
        {"appName": "Netscape", "major": "220", "name": "Facebook", "version": "220.0.0.20.121"}
    ]

    population_update_rates = [
        (0.5, 52), (0.35, 41), (0.1, 33), (0.05, 23)
    ]

    def update(self):
        cur_version = float(self.value["version"])
        random_upgrade = round(random.uniform(0, 0.1), 2)
        cur_version = round(cur_version + random_upgrade, 1)
        self.value["version"] = str(cur_version)
        self.value["major"] = str(int(cur_version))

class OSFeature(metaclass=FeatureMeta):
    possible_values = [
        { "name": "Windows", "version": "10" },
        { "name": "Mac OS", "version": "10.14" },
        {"name": "Android", "version": "7.0"},
        {"name": "iOS", "version": "12.3.1"},
        {"name": "Ubuntu", "version": "18.0.4"}
    ]

class UAFeature(metaclass=FeatureMeta):
    possible_values = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.101 Mobile Safari/537.36 [FB_IAB/Orca-Android;FBAV/220.0.0.20.121;]",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
    ]  

class ColorDepthFeature(metaclass=FeatureMeta):
    possible_values = [
        8,
        16,
        24
    ]    

class DeviceFeature(metaclass=FeatureMeta):
    possible_values = [
        {
        "model" : "iPhone",
        "type" : "mobile",
        "vendor" : "Apple"
      },
      {
        "model" : "WAS-LX3",
        "type" : "mobile",
        "vendor" : "Huawei"
      },
      {
        "model" : "PRA-LX1",
        "type" : "mobile",
        "vendor" : "Huawei"
      },
      {
        "model" : "E1003",
        "type" : "mobile",
        "vendor" : "Sony"
      },
      {
        "model" : "SM-N9208",
        "type" : "mobile",
        "vendor" : "Samsung"
      }
    ]

class EngineFeature(metaclass=FeatureMeta):
    possible_values = [
        {
        "name" : "Gecko",
        "version" : "67.0"
        },
        {
        "name" : "WebKit",
        "version" : "605.1.15"
      },
      {
        "name" : "EdgeHTML",
        "version" : "17.17134"
      }
    ]    

class CPUFeature(metaclass=FeatureMeta):
    possible_values = [
        {
        "architecture" : "amd64"
      }
    ]    

class BrowserInstance():
    def __init__(self):
        # This number will define in which kind of profile does this browser fall : casual / rare ?
        # Will drive features updates frequency
        self.singularity_ratio = random.random()
        self.id = str(uuid.uuid4())
        self.features = {
            "acceptedCharset": AcceptedCharsetFeature(self.singularity_ratio),
            "acceptedEncoding": AcceptedEncodingFeature(self.singularity_ratio),
            "acceptedMime": AcceptedMimeFeature(self.singularity_ratio),
            "acceptedLanguages": AcceptedLanguagesFeature(self.singularity_ratio),
            "doNotTrack": DoNotTrackFeature(self.singularity_ratio),
            "screenSize": ScreenSizeFeature(self.singularity_ratio),
            "innerSize": InnerSizeFeature(self.singularity_ratio),
            "outerSize": OuterSizeFeature(self.singularity_ratio),
            "plugins": PluginsFeature(self.singularity_ratio),
            "timezoneOffset": TimezoneOffsetFeature(self.singularity_ratio),
            "browser": BrowserFeature(self.singularity_ratio),
            "os": OSFeature(self.singularity_ratio),
            "ua": UAFeature(self.singularity_ratio),
            "device": DeviceFeature(self.singularity_ratio),
            "colorDepth": ColorDepthFeature(self.singularity_ratio),
            "cpu": CPUFeature(self.singularity_ratio),
            "engine": EngineFeature(self.singularity_ratio)
        }

        # Other features will keep their initial random value
        self.mutable_features = [
            self.features["browser"],
            self.features["plugins"],
            self.features["screenSize"],
            self.features["innerSize"],
            self.features["outerSize"],
            self.features["timezoneOffset"],
            self.features["acceptedEncoding"],
            self.features["acceptedMime"],
            self.features["acceptedLanguages"]
        ]

        self.history = [self.toJson(0)]

    def check_for_updates(self, day):
        random.shuffle(self.mutable_features)
        updates = 0
        for feature in self.mutable_features:
            if updates >= 2: # No more than 2 updates at the same time
                break
            if feature.check_for_updates(day):
                updates += 1

        if updates > 0: # save this new fingerprint if it has been updated
            self.history.append(self.toJson(day))
        return self

    def toJson(self, day=None):
        fingerprint = copy.deepcopy({
            key: feature.value for key, feature in self.features.items()
        })
        if day is not None:
            fingerprint["day"] = day
        fingerprint["browser_id"] = self.id
        fingerprint["uaInfo"] = {
            "device": self.features["device"].value,
            "engine": self.features["engine"].value,
            "os": self.features["os"].value,
            "ua": self.features["ua"].value,
            "browser": self.features["browser"].value,
            "cpu": self.features["cpu"].value,
        }
        del fingerprint["ua"]
        del fingerprint["device"]
        del fingerprint["engine"]
        del fingerprint["os"]
        del fingerprint["browser"]
        del fingerprint["cpu"]
        return fingerprint


def generate(nb_browsers, nb_days, only_last_fingerprints=False):
    browsers = [BrowserInstance() for _ in range(nb_browsers)]
    for i in range(nb_days):
        browsers = [browser.check_for_updates(i) for browser in browsers]
    if not only_last_fingerprints:
        fingerprints = list(
            itertools.chain(*(cur.history for cur in browsers))
        )
        random.shuffle(fingerprints)
        return fingerprints
    return [cur.toJson() for cur in browsers]

def generate_formatted_fingerprints(nb_browsers=20, nb_days=100):    
    fingerprints = generate(nb_browsers, nb_days)
    # map fingerprints to browser_id
    fingerprints = [
        DataEncoder(fingerprint).m_formated_data for fingerprint in fingerprints
    ]
    
    return fingerprints
    # print("Generated {} fingerprints".format(len(fingerprints)))

if __name__ == "__main__":
    plac.call(generate_formatted_fingerprints)