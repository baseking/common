#!/usr/bin/python
#coding:utf-8
import time
import consmin as ct
import os
#import calendar
#import random as rn
#import pandas as pd
from datetime import datetime
import re
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
def grab_dpmf():
    index_list = ['sh','sz','zxb','cy','B','szn','hs300','i100','sz50','dpmf']
    index_str_list = ['sh000001','sz399001','sz399005','sz399006','sh000003','sz399678','sz399300','sz399415','sh000016','dpmf'] 
    index_use_zdp =[1,1,1,1,0,1,0,0,0,0]
    
    trade_list = index_list
    #B指数的涨跌平数有沪深两个，比较麻烦，不处理
    index_str = ''
    zdp_str = ''
    zdp_len = 0
    zdp_list = []
    zdp_index_list = []
    for index,x in enumerate(index_str_list):
        index_str = index_str + x + ','
        if index_use_zdp[index]:
            zdp_index_list.append(zdp_len)
            zdp_len = zdp_len + 1
            zdp_str = zdp_str + x + '_zdp,' 
            zdp_list.append(index_list[index])
        else:
            zdp_index_list.append(0)
    trade_str = index_str +zdp_str

    line_chars = '\r\n'#换行符
    while(1):
        #初始化
        ttype = 0
        trade_time = '09:15:01'
        last_time = '09:00:00'
        print("start")
        #判断当前时间
        while(ttype in [0,1,7]):
            #now_time = time.strftime('%H:%M:%S',time.localtime())
            now_time = datetime.utcfromtimestamp(time.time()+28800).strftime("%H:%M:%S")
            ttype = trade_type(now_time)    
            print("not in  trade"+ttype.__str__())
            time.sleep(ct.TIME_END)
        #每日日志文件
        #now_date = time.strftime('%Y-%m-%d',time.localtime())
        now_date = datetime.utcfromtimestamp(time.time()+28800).strftime("%Y-%m-%d")
        log_path = 'log//index//' + now_date + '.txt'
        try:
            f1 = open(log_path,'a+')#避免中间启动，故用a而不用w
        except:
            print(log_path + 'file open error')
            exit(0)
        print(log_path + 'file open')
        f1.write("start at:{:s} {:s}{:s}".format(now_date,now_time,line_chars))
        f1.flush()
        #开始每日采集
        request_url = ct.LIVE_DATA_URL%(ct.P_TYPE['http'], ct.DOMAINS['sinahq'],_random(), trade_str)
        request = Request(request_url)
        
        work_flag = 1
        rec_flag = 0
        shaked_flag = 0
        is_to_delete = 1
        while(work_flag):
            now_time = datetime.utcfromtimestamp(time.time()+28800).strftime("%H:%M:%S")
            #now_time = time.strftime('%H:%M:%S',time.localtime())
            if (now_time > '15:00:06' and ttype == 7) and rec_flag:
                print('not trade time,quit，present time:%s' % now_time)
                work_flag = 0
                #f1.close()
                work_flag = 0
            elif ttype == 3 and not shaked_flag:#撮合阶段，只保存一次
                work_flag = 1
                shaked_flag = 1
                is_to_delete = 0
                time.sleep(ct.TIME_PAUSE)
            elif ttype in [2,5] and rec_flag:#暂停阶段或未开始
                work_flag = 1
                ttype = trade_type(now_time)
                time.sleep(ct.TIME_PAUSE)
                continue
            elif ttype in [4,6] and rec_flag:#交易阶段
                work_flag = 1
                is_to_delete = 0
                time.sleep(ct.TIME_TRADE)
                ttype = trade_type(trade_time)
            else:
                work_flag = 1
                ttype = trade_type(now_time)
                if rec_flag:
                    time.sleep(ct.TIME_TRADE)
                    continue
            try:
                text = urlopen(request,timeout=ct.TIMEOUT).read()
            except:
                print('network error,timeout，present time:%s' % now_time)
                continue
            rec_flag = 1#执行到这里
            text = text.decode('GBK')
            reg = re.compile(r'\="(.*?)\";')
            reg1 = re.compile(r'[0-9]+')
            data = reg.findall(text)
            regSym = re.compile(r'(?:sh|sz/dp)(.*?)\=')
            syms = regSym.findall(text)
            data_list = []
            syms_list = []
            isdata = 0
            for index, row in enumerate(data):
                data_list.append([astr for astr in row.split(',')])
                l = len(data_list[index])
                if l < 33:
                    data_list[index] = data_list[index] + [None]*(33-l)
                try:
                    data_list[index].append(trade_list[index])
                except:
                    pass
            try:
                trade_time = max([t[31] for t in data_list[:4]])
                trade_date = max([t[30] for t in data_list[:4]])
                print(trade_date)
            except:
                trade_time = now_time
            l1 = len(data_list)
            i = 0
            if (l1 < len(index_list[:-1])):
                print('length error，maybe network error,present time:%s' % trade_time)
                continue
            #显示指数
            nt = int(time.time()) + ct.BJ_TIMESTAMP_OFFSET
            all_money = 0
            str_index = "{:s}-{:s}\t".format(now_time,trade_time)
            pre_index_len = len(index_list[:-1])
            for i,x in enumerate(index_list):
                if i < pre_index_len:
                    try:
                        rate = (float(data_list[i][3])/float(data_list[i][2]))*100 - 100
                    except:
                        rate =0
                    money = reg1.findall(data_list[i][9])[0][:-6]
                    if len(money) < 1:
                        money = '0'
                    all_money = all_money + int(money)
                    
                    if index_use_zdp[i]:
                        zdp_index = zdp_index_list[i]+pre_index_len+1
                        str1 = "{:s}({:s},{:.2f},{:s},{:s},{:s})\t".format(index_list[i],data_list[i][3],rate,data_list[zdp_index][0],data_list[zdp_index][1],data_list[zdp_index][2])
                    else:
                        str1 = "{:s}({:s},{:.2f})\t".format(index_list[i],data_list[i][3],rate)
                    str_index = str_index + str1 +'\t'
                else:#显示资金流动
                    if all_money >0:
                        all_rate = (float(data_list[pre_index_len][0])/(all_money/100))*100
                    else:
                        all_rate = 0.0
                    str1 = "dpmf({:s},{:.2f}){:s}".format(data_list[pre_index_len][0],all_rate,line_chars)
                    str_index = str_index + str1
                
                    if trade_time > last_time:#确保有变动才写日志               
                        f1.write(str_index)

                        if now_date > trade_date:
                            work_flag = 0
                            is_to_delete = 1
                        f1.flush()
                        last_time = trade_time
                    else:
                        print("not change")
        if not work_flag:
            try:
                f1.write("end at:{:s} {:s}{:s}".format(now_date,now_time,line_chars))
                f1.close()
                if is_to_delete:
                    os.remove(log_path)
                    print("not trade date,remove log file")
            except:
                pass             
def trade_type(t="09:00:00"):
    """
    0:=00:00->09:15 before trade time
    1:=09:15->09:25 shake time
    2:=09:25->09:26 shake deal time
    3:=09:26->09:30 wait trade free
    4:=09:30->11:30 morning trade free time
    5:=11:30->13:00 midday breaktime
    6:=13:00->15:00 afternoon trade free time
    7:=15:00->24:00 after trade rest time
    """
    ttype = 0
    if t < "24:00:00":
        for i in ct.TRADE_TIME:
            if i > t:
                ttype = ct.TRADE_TIME.index(i) - 1
                break
    return ttype
def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))
if __name__ == "__main__":
    grab_dpmf()
