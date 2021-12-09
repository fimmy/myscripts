from genericpath import exists
import tomli, os

conf = {}
config = {}
try:
    confpath = "/data/fimmy_data/conf.toml"
except:
    confpath = "conf.toml"
try:
    if os.path.exists(confpath):
        with open(confpath, "rb") as conf:
            config = tomli.load(conf)
except:
    pass
