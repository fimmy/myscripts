from load_config import config
from send_notice import sendNotice
import requests, json, re
from load_config import config

useragent = "Kuaikan/5.75.0/575000(iPhone;Scale/3.00) (iPhone; CPU)"


def giftpack(type, cookie):
    message = ""
    regex = r'今(日|天)可领'
    match = re.search(regex, type)
    if not match:
        return ""
    else:
        url = "https://h5.kuaikanmanhua.com/v1/checkin/api/check/open_gift_bag"
        gitpackResponse = requests.get(url,
                                       headers={
                                           'Cookie': cookie,
                                           'User-Agent': useragent,
                                           'X-Device': '0'
                                       })
        if gitpackResponse.ok:
            gift = json.loads(gitpackResponse.content)
            if gift["code"] == 200:
                data = gift["data"]
                message += "领取连签礼包成功"
                if "giftBagScore" in data:
                    tmpm = data["giftBagScore"]
                    message += f",{tmpm}积分"
                if "giftBagKkb" in data:
                    tmpm = data["giftBagKkb"]
                    message += f",{tmpm}KK币"
                if "giftBagSupplement" in data:
                    message += ",+1 补签胶囊"
                if "giftBagSupplement" in data:
                    tmpm = data["cardCoupon"]["title"]
                    message += ",+1 {tmpm}"
                if "giftBagYouzanCoupon" in data:
                    tmpm = data["youzanCoupon"]["title"]
                    message += ",+1 {tmpm}"
            else:
                if "message" in gift:
                    msg = gift["message"]
                message += f"领取连签礼包失败,{msg} "
        else:
            message += "领取连签礼包错误"


def checkin(conf):
    cookie = conf["cookie"]
    notice = conf["notice"]
    user = conf["user"]
    nickName = conf["nickName"]
    uidMatch = re.search('uid=(\d+)', cookie)
    if uidMatch:
        uid = uidMatch.group(1)
    url = "https://h5.kuaikanmanhua.com/v2/checkin/task_center/checkin"

    message = "快看漫画签到:\n"

    checkinResponse = requests.get(url,
                                   headers={
                                       'Cookie': cookie,
                                       'User-Agent': useragent,
                                       'X-Device': '0'
                                   })
    if checkinResponse.ok:
        checkin = json.loads(checkinResponse.content)
        code = checkin["code"]
        if code == 200:
            message += ""
            checkinInfo = checkin["data"]["check_in_home_info"]
            pop = checkinInfo["pop_title"]
            text = checkinInfo["check_in_bubble_text"]
            title = checkinInfo["check_in_title"]
            score = checkinInfo["user_score"]
            kkb = checkinInfo["user_kkb"]
            gift = giftpack(title, cookie)
            message += f"{nickName}-用户id:{uid}:\n{text},现有{score}积分, {kkb}KK币\n{gift}{title} 🎉"
        elif code == 401:
            message += "cookies失效"
        else:
            message += "未知错误"
    else:
        message += "未知错误"
    if notice:
        sendNotice(message, user)


def start():
    confs = config["kkmh"]
    for conf in confs:
        checkin(conf)


if __name__ == '__main__':
    start()
