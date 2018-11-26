# # foo = ['a','b','c','d','e']
# # from random import choice
# # print(choice(foo))
# import os,sys
# import random
# import configparser
# ConfPath = "Conf/binstream.conf"
#
# if not  os.path.exists(ConfPath):
#     sys.exit("%s not found" %ConfPath )
# cf = configparser.ConfigParser()
# cf.read(ConfPath)
#
#
# CacheHost = cf.get('SC','CacheHostID')
# MKHost = cf.get('MK','MKHostID')
# SOHost = cf.get('SO','SOHostID')
#
# #生成列表
# CacheHostIDList = CacheHost.split(',')
# MKHostIDList = MKHost.split(',')
# SOHostList = SOHost.split(',')
# # print(CacheHostIDList)
# # print(MKHostIDList)
#
# #随机挑选服务器发布、加速、秒开
# CacheHostID = random.choice(CacheHostIDList)
# MKHostID = random.choice(MKHostIDList)
# SOHostID = random.choice(SOHostList)
#
# print(CacheHostID)
# print(MKHostID)
# print(SOHostID)
#

# import threading
# from time import ctime,sleep
#
#
# def music(func):
#     for i in range(2):
#         print ("I was listening to %s. %s" %(func,ctime()))
#         sleep(1)
#
# def move(func):
#     for i in range(2):
#         print ("I was at the %s! %s" %(func,ctime()))
#         sleep(5)
#
# threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
# t2 = threading.Thread(target=move,args=(u'阿凡达',))
# threads.append(t2)
#
# if __name__ == '__main__':
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#     t.join()
#     print ("all over %s" %ctime())
import os
filename = 'id.txt'
if not os.path.exists(filename):
    print("%s不存在" % filename)
else:
    print("%s 存在" % filename)

with open(filename,'r+',encoding='utf-8') as f:
    first_line = f.readline()
    print(first_line)
    f.close()

with open(filename,'w+',encoding='utf-8') as f:
    f.write("123459")
    f.close()

    #print(lines[0])