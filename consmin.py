#!/usr/bin/python
#coding:utf-8
P_TYPE = {'http': 'http://', 'ftp': 'ftp://'}
INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500','i100']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sz399300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006', 'zx300': 'sz399008', 'zh500':'sh000905','i100':'sz399415'}
LIVE_DATA_URL = '%shq.%s/rn=%s&list=%s'
DOMAINS = {'sina': 'sina.com.cn', 'sinahq': 'sinajs.cn',
           'ifeng': 'ifeng.com', 'sf': 'finance.sina.com.cn',
           'vsf': 'vip.stock.finance.sina.com.cn', 
           'idx': 'www.csindex.com.cn', '163': 'money.163.com',
           'em': 'eastmoney.com', 'sseq': 'query.sse.com.cn',
           'sse': 'www.sse.com.cn', 'szse': 'www.szse.cn',
           'oss': '218.244.146.57', 'idxip':'115.29.204.48',
           'shibor': 'www.shibor.org', 'mbox':'www.cbooo.cn'}
PAGES = {'fd': 'index.phtml', 'dl': 'downxls.php', 'jv': 'json_v2.php',
         'cpt': 'newFLJK.php', 'ids': 'newSinaHy.php', 'lnews':'rollnews_ch_out_interface.php',
         'ntinfo':'vCB_BulletinGather.php', 'hs300b':'000300cons.xls',
         'hs300w':'000300closeweight.xls','sz50b':'000016cons.xls',
         'dp':'all_fpya.php', '163dp':'fpyg.html',
         'emxsg':'JS.aspx', '163fh':'jjcgph.php',
         'newstock':'vRPD_NewStockIssue.php', 'zz500b':'000905cons.xls',
         'zz500wt':'000905closeweight.xls',
         't_ticks':'vMS_tradedetail.php', 'dw': 'downLoad.html',
         'qmd':'queryMargin.do', 'szsefc':'ShowReport.szse',
         'ssecq':'commonQuery.do', 'sinadd':'cn_bill_download.php', 'ids_sw':'SwHy.php'}
TRADE_TIME = ['00:00:00','09:15:00','09:25:00','09:26:00','09:30:00','11:30:00','13:00:00','15:00:00','24:00:00']
TRADE_TIME = ['00:00:00','09:15:00','09:25:00','09:26:00','09:30:00','11:30:00','13:00:00','15:00:00','24:00:00']
TIMEOUT = 20#15s
BJ_TIMESTAMP_OFFSET = 28800
TIME_PAUSE = 30#交易暂停
TIME_END = 100#交易结束
TIME_TRADE = 30#交易时间
