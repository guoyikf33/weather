import simplejson as json
import requests
import datetime
import fake_useragent # 这个库可以不用
from bs4 import BeautifulSoup
import time

def get_fake_ua(): #这个函数是用来获取随机UA的，可以不用
    location = 'fake_useragent_0.1.11.json' #这里是我导入的fakeuseragent库文件，可以不用
    ua = fake_useragent.UserAgent(path=location)

    headers = {
        'user-agent': ua.random
    }
    return headers

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return "今天日期为：" + str(datetime.date.today()) + ' ' + week_day_dict[day]

def get_weather():
    url = "https://d1.weather.com.cn/sk_2d/101020100.html?_=1618886817920"
    r_url = requests.get(url, headers=get_fake_ua())
    message = json.loads(r_url.text.encode("latin1").decode("utf8").replace("var dataSK = ", ""))
    cityname = message['cityname']
    aqi = int(message['aqi'])
    sd = message['sd']
    wd = message['WD']
    ws = message['WS']
    temp = message['temp']
    weather = message['weather']
    if aqi <= 50:
        airQuality = "优"
    elif aqi <= 100:
        airQuality = "良"
    elif aqi <= 150:
        airQuality = "轻度污染"
    elif aqi <= 200:
        airQuality = "中度污染"
    elif aqi <= 300:
        airQuality = "重度污染"
    else:
        airQuality = "严重污染"
    return cityname + " " + '今日天气：' + weather + ' 温度：' + temp + ' 摄氏度 ' + wd + ws + ' 相对湿度：' + sd + ' 空气质量：' \
           + str(aqi) + "（" + airQuality + "）"

def get_top_list():
    requests_page = requests.get('http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b42_c513')
    soup = BeautifulSoup(requests_page.text,"lxml")
    soup_text = soup.find_all("a", class_='list-title')
    i = 0
    top_list = []
    for text in soup_text:
        i += 1
        top_list.append(text.string.encode("latin1").decode("GBK"))
        if i == 10:
            break
    return top_list

def get_daily_sentence():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url, headers=get_fake_ua())
    r = json.loads(r.text)
    content = r["content"]
    note = r["note"]
    daily_sentence = content + "\n" + note
    return daily_sentence

def get_sendContent():
    sendContent =  get_week_day(datetime.date.today()) + "\n\n" + get_weather() + "<br>" + str(get_top_list()).replace(
        "', '", '\n').replace("['", "").replace("']", "") + "<br>" + get_daily_sentence()
    return sendContent
    
def send(content):
    url = "http://pushplus.hxtrip.com/send"
    headers = {"Content-Type": "application/html"}
    data = {
        "token": "dc5b5401e1eb4464982a8dc286f2d25b",
        "title": "每日推荐",
        "content": content,
        "template":"html",
        "topic":"Weather"
    }
    requests_url = requests.post(url, headers=headers, data=json.dumps(data))
    if requests_url.text == '{"errcode":0,"errmsg":"ok"}':
        return "发送成功"
    else:
        return "发送失败" + requests_url.text

print(send(get_sendContent()))