import requests
from load_config import config


def sendNotice(content, user):
    if len(content) == 0 or len(user) == 0:
        return
    url = config["notice"]["url"]
    url = url.replace("{text}", content)
    url = url.replace("{user}", user)
    requests.get(url)
