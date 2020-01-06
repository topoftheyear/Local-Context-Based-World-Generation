import random
import threading

import numpy as np


class Thread(threading.Thread):
    def __init__(self, func, args=list()):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        
    def run(self):
        self.func(*self.args)


def random_bool(denominator=1):
    return random.randint(0, max(0, denominator)) == 0


def clamp(num, mini=0, maxi=1):
    return max(mini, min(num, maxi))


def merge_sum_dictionaries(dict1, dict2):
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}


def weighted_random_from_dict(d):
    total = sum(d.values())
    keys = [int(k) for k in d.keys()]
    weights = [k / total for k in d.values()]
    return np.random.choice(keys, p=weights)
