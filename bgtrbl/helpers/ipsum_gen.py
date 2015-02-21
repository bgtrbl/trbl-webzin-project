import os
import random
from os.path import realpath, join, split

def _getData(filename):
    with open(filename, 'r') as f:
        return f.readlines()

_FILENAMES = ["data/post.txt", "data/post_ko.txt"]

_DATA = [_getData(f)[0] for f in _FILENAMES]
_DATA = [ data.replace(".", "").split() for data in _DATA]

def flat(g):
    return [_ for _ in g]


def word(c, l=True):
    for _ in range(c):
       yield random.choice(_DATA[l])


def sen(c, l=True, r=None):
    if r is None:
        r = range(14, 40)
    return (" ".join(flat(word(random.choice(r), l=l))) + "." for _ in range(c))


def para(c, l=True, r=None):
    if r is None:
        r = range(5,10)
    return (" ".join(flat(sen(random.choice(r), l=l))) for _ in range(c))
