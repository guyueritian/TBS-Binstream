#coding=utf-8
from urllib import request
from urllib import parse
import MySQLdb
import json
import configparser
import PubBinstream as PubBS
import os,sys,time
import threading
srs_api = "http://144.217.252.235:16161/api/v1/streams/"
srs_ip = "144.217.252.235"
srs_port = "1935"

ID_Value_File = 'id.txt'    #记录chid值，没发布完一个频道都会递增并保存到该文件
DBConfPath = 'Conf/db.conf'

if not os.path.exists(DBConfPath):
    sys.exit("%s Not Found！" % DBConfPath)
dbcf = configparser.ConfigParser()
dbcf.read(DBConfPath)

dbhost = dbcf.get('conf_db', 'host')
dbusername = dbcf.get('conf_db', 'user')
dbpassword = dbcf.get('conf_db', 'password')
dbbase = dbcf.get('conf_db', 'database')

# dbhost = '142.44.136.80'
# dbusername = 'root'
# dbpassword = 'malaitestforce'
# dbbase = 'livecms'

class Mysqldb(object):
    def __init__(self, dbhost, dbusername, dbpassword, dbbase):
        self.dbhost = dbhost
        self.dbusername = dbusername
        self.dbpassword = dbpassword
        self.dbbase = dbbase

    def connection(self):
        try:
            db = MySQLdb.connect(self.dbhost, self.dbusername, self.dbpassword, self.dbbase, charset="utf8")
        except:
            return False
        else:
            return db

    def select(self, dbsql):
        if self.connection():
            db = self.connection()
            cursor = db.cursor()
            cursor.execute(dbsql)
            results = cursor.fetchall()
            db.close()
            return results
        else:
            return -1

    def action(self, dbsql):
        if self.connection():
            try:
                db = self.connection()
                cursor = db.cursor()
                cursor.execute(dbsql)
                print(dbsql)
            except:
                db.rollback()
                return False
            else:
                db.commit()
                return True
            finally:
                db.close()
        else:
            return -1


def Get_Info():
    try:
        url = srs_api
        rq = request.Request(url)
        res = request.urlopen(rq)
        respoen = res.read()
        result = str(respoen,encoding='utf-8')
        #print(result)
        return result
    except Exception as err:
        print('Exception：',err)
#Get_Info()
PubUrl = 'http://manage.hdtvvip.com:5010/apiv1/channel'
# chid = 123457
# sid = 123457

def Inset_Into_DB():
    #每次发布都会从文件中获取到chid
    with open(ID_Value_File, 'r+', encoding='utf-8') as f:
        first_line = int(f.readline().strip())
        print(first_line)
        f.close()
    chid = first_line
    sid = first_line
    ApiInfo = Get_Info()
    Json_ApiInfo = json.loads(ApiInfo)
    Channel_Info = Json_ApiInfo['streams']
    for dic in Channel_Info:
        spingyin = dic['name']
        #print("rtmp://%s:%s/push/%s" % (srs_ip,srs_port,spingyin))
        rtmpurl = "rtmp://%s:%s/push/%s" % (srs_ip,srs_port,spingyin)
        print(rtmpurl)
        db = Mysqldb(dbhost,dbusername,dbpassword,dbbase)
        dbselect_result = db.select("SELECT url from force_video WHERE url = \'%s\'" % rtmpurl)
        print(len(dbselect_result))

        if len(dbselect_result) == 0:
            print("开始发布频道%s" % chid)
            PubBS.Post(PubBS.PubUrl,PubBS.cookie_filename,PubBS.p2p_originator,rtmpurl,PubBS._type,spingyin,chid,sid)

            print("开启频道%s" % chid)
            PubBS.Start("http://manage.hdtvvip.com:5010/apiv1/channel/%s/start" % chid,PubBS.cookie_filename)
            time.sleep(5)

            print("获取频道tvbus地址%s" % chid)
            ID_Tvbus_Result = PubBS.GetID_Tvbus(chid)
            _id = ID_Tvbus_Result[1]
            tvbus = ID_Tvbus_Result[0]

            print("开启频道加速%s" % chid)
            PubBS.Start("http://manage.hdtvvip.com:5010/apiv1/channelcache/%s/start/%s" % (chid, PubBS.CacheHostID),PubBS.cookie_filename)

            print("开启频道秒开%s" % chid)
            PubBS.Start("http://manage.hdtvvip.com:5010/apiv1/chmkcache/%s/start/%s" % (chid, PubBS.MKHostID), PubBS.cookie_filename)
            chid = chid + 1
            sid = sid + 1
            with open(ID_Value_File, 'w+', encoding='utf-8') as f:
                f.write(str(chid))
                f.close()

            print("---------------------数据获取完毕---------------------")
            print("节目id为%s：" % _id)
            print("节目名字（这里为拼音缩写）：%s" % spingyin)
            print("节目源地址为：%s" %rtmpurl )
            print("tvbus地址为：%s" % tvbus)

            print("-------------->开始插入数据<--------------")
            dbselect_result = db.action("INSERT INTO force_video (id,name,url,p2p_url,create_time) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',NOW())" %(_id,spingyin,rtmpurl,tvbus))
            print(dbselect_result)



if __name__ == '__main__':
    t = threading.Thread(target=Inset_Into_DB())
    t.setDaemon(True)
    t.start()
