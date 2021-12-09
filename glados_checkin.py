from load_config import config
from send_notice import sendNotice
import requests, json
from load_config import config


def checkin(conf):
    cookie = conf["cookie"]
    notice = conf["notice"]
    user = conf["user"]
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload = {'token': 'glados_network'}
    checkinResponse = requests.post(url,
                                    headers={
                                        'cookie':
                                        cookie,
                                        'referer':
                                        referer,
                                        'origin':
                                        origin,
                                        'user-agent':
                                        useragent,
                                        'content-type':
                                        'application/json;charset=UTF-8'
                                    },
                                    data=json.dumps(payload))
    if checkinResponse.ok:
        checkin = json.loads(checkinResponse.content)
    stateResponse = requests.get(url2,
                                 headers={
                                     'cookie': cookie,
                                     'referer': referer,
                                     'origin': origin,
                                     'user-agent': useragent
                                 })
    if stateResponse.ok:
        state = json.loads(stateResponse.content)
    message = "GLADOS 签到:\n"
    if 'message' in checkin:
        mess = checkin['message']
        leftDay = state['data']['leftDays']
        leftDay = leftDay.split('.')[0]
        if (checkin["code"] < 0):
            message += "cookie过期:" + mess
        else:
            message += "签到成功：" + mess + "\n剩余：" + leftDay + "天"
    else:
        message += 'cookie过期'
    if notice:
        sendNotice(message, user)


def start():
    confs = config["glados"]
    for conf in confs:
        checkin(conf)


if __name__ == '__main__':
    start()
