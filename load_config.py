from genericpath import exists
import tomli, os

conf = {}
config = {}
if os.path.exists("/data/fimmy_data/conf.toml"):
    confpath = "/data/fimmy_data/conf.toml"
else:
    confpath = "conf.toml"
print(f"读取配置文件:{confpath}")
try:
    if os.path.exists(confpath):
        with open(confpath, "rb") as conf:
            config = tomli.load(conf)
except Exception as ex:
    print(f"读取配置文件发生异常:" + str(ex))
    pass
