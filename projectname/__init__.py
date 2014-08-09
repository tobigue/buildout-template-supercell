import json

with open("conf/options.json") as f:
    __options__ = json.load(f)

__version__ = tuple(__options__["general"]["version"].split("."))
