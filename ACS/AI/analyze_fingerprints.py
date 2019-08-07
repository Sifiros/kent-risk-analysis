#!/usr/local/bin/python3
import json
import plac

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def analyze_fingerprints(user_id: "User's fingerprints to analyze"):
    with open("models/{}/fingerprints.json".format(user_id), "r") as f:
        fingerprints = json.loads(f.read())

    fingerprints = sorted(fingerprints, key=lambda cur: cur['day'])
    i = 1
    while i < len(fingerprints):
        day_a = fingerprints[(i - 1)]
        day_b = fingerprints[i]
        diff = DictDiffer(day_a, day_b)
        print("From day {} to {}, diffs : ".format(day_a["day"], day_b["day"]))
        print(diff.changed())
        i += 1

if __name__ == "__main__":
    plac.call(analyze_fingerprints)
    