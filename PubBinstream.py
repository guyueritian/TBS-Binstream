import json
import urllib
from urllib import request
from urllib import error
from http import cookiejar
from urllib import parse
import os,sys
import random
import configparser

cookie_filename = 'cookie.txt'
ConfPath = "Conf/binstream.conf"

if not  os.path.exists(ConfPath):
    sys.exit("%s Not Found" % ConfPath )
cf = configparser.ConfigParser()
cf.read(ConfPath)


CacheHost = cf.get('SC','CacheHostID')
MKHost = cf.get('MK','MKHostID')
SOHost = cf.get('SO','SOHostID')

CacheHostIDList = CacheHost.split(',')
MKHostIDList = MKHost.split(',')
SOHostList = SOHost.split(',')

CacheHostID = random.choice(CacheHostIDList)
MKHostID = random.choice(MKHostIDList)
SOHostID = random.choice(SOHostList)

if not  os.path.exists(ConfPath):
    sys.exit("%s not found" %ConfPath )
cf = configparser.ConfigParser()
cf.read(ConfPath)



def GetCookie():
    cookie_filename = 'cookie.txt'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
               'Referer': 'http://manage.hdtvvip.com:5010'}
    data = {
        "username": "evpad",
        "password": "evpad123"
    }
    login_url = 'http://manage.hdtvvip.com:5010/login'
    post_data = urllib.parse.urlencode(data).encode('utf-8') # 提交类型不能为str，需要为byte类型
    cookie = cookiejar.MozillaCookieJar(cookie_filename)
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    req = request.Request(login_url,post_data,headers)
    try:
        response = opener.open(req)
    except urllib.error.URLError as e:
        print(e.reason)
    cookie.save(ignore_discard=True,ignore_expires=True)
    for item in cookie:
        _cookie = item.value
        print(_cookie)
#GetCookie()

p2p_originator = SOHostID
source_address = 'rtmp://144.217.252.235:1935/push/zsjd'
_type = 1
# name = 'aaa'
# chid = 123456
# sid = 123456
PubUrl = 'http://manage.hdtvvip.com:5010/apiv1/channel'
#发布频道
def Post(url,cookie_filename,p2p_originator,source_address,_type,name,chid,sid):
    GetCookie()
    data = {
        'p2p._originator' : '%s' % p2p_originator,
        'source._address' : '%s' % source_address,
        'type' : '%d' % _type,
        'name.init' : '%s' % name,
        'chid' : '%d' % chid,
        'sid' : '%d' % sid ,
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
               'Referer': 'http://manage.hdtvvip.com:5010'}
    PubUrl = url
    cookie_filename = cookie_filename
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    cookie = cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)  #解析字符串为Cookie数据
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    req = request.Request(url=PubUrl,data=post_data,headers=headers,method="POST")
    try:
        response = opener.open(req)
        #print(response.read())
        #print("发布频道：%s  chid：%s，" %(name,chid))
        print(response.code)
    except urllib.error.URLError as e:
        print(e.reason)

#Post(PubUrl,cookie_filename,p2p_originator,source_address,type,name,chid,sid)

#开启频道、SC、MK
def Start(url,cookie_filename):
    get_url = url
    cookie_filename = cookie_filename
    cookie = cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    get_request = urllib.request.Request(method="GET", url=get_url)
    try:
        response = opener.open(get_request)
        print(response.read())
    except  urllib.error.URLError as e:
        print(e.reason)

#开启加速
#Start("http://manage.hdtvvip.com:5010/apiv1/channel/%s/start" % 123456,cookie_filename)

#开启加速
#CacheHostID = CacheHostID
#Start("http://manage.hdtvvip.com:5010/apiv1/channelcache/%s/start/%s" % (chid,CacheHostID),cookie_filename)

#开启秒卡
#MKHostID = MKHostID
#Start("http://manage.hdtvvip.com:5010/apiv1/chmkcache/%s/start/%s" % (chid,MKHostID),cookie_filename)

#获取TVBUS地址
def Get_Channel_Info(url,cookie_filename):
    get_url = url
    cookie_filename = cookie_filename
    cookie = cookiejar.MozillaCookieJar(cookie_filename)
    cookie.load(cookie_filename,ignore_discard=True,ignore_expires=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    get_request = urllib.request.Request(get_url)
    get_response = opener.open(get_request)
    channel_info = get_response.read().decode('utf-8')
    global jsondata
    jsondata = json.loads(channel_info)


def GetID_Tvbus(_chid):
    #ID_Tvbus_Dic = {}
    Get_Channel_Info('http://manage.hdtvvip.com:5010/apiv1/channel?populate=group', cookie_filename)
    for dictionary in jsondata:
        chid = int(dictionary["chid"])
        if chid == _chid:
            tvbus = dictionary["source"]["address"]
            #_name = dictionary["name"]["init"]
            _id = dictionary["_id"]
            if tvbus == "":
                #tvbus = "节目源故障"
                tvbus = "None"
            #生成节目id和tvbus地址的对应字典
    #print(ID_Tvbus_Dic)
    return (tvbus,_id)
#a=GetID_Tvbus(123456)
#print(a)
