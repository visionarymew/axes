#进行代理抓取和初步测试

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import os
import json

def gethtml(url):
    try:
        agent =[
            {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'},
            {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'},
            {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'},
                ]
        a = requests.get(url, headers = random.choice(agent), timeout=50)
        a.raise_for_status()
        return a.text
    except:
        print(datetime.now(),'gethtmltext error')

def getproxy():

    url1=['http://www.goubanjia.com/free/gngn/index%s.shtml'%x for x in range(1,10) ]
    url2=['http://www.xicidaili.com/nn/'+str(x) for x in range(1,10)]
    #字典格式 key = 'ip:port' value = [http]
    proxydic = {}


    for url in url1:
        proxy_gbj(url,proxydic)

    #被ban了= =
    #for url in url2:
    #    proxy_xcdl(url,proxydic)
    n = 0
    for p in proxydic:
        #测试是否能使用，能使用保存为JSON数据
        proxy = proxy_test(n,p,proxydic)
        if proxy:
            proxy_save(proxy,proxydic)


def proxy_gbj(url,proxydic):
    soup = BeautifulSoup(gethtml(url), 'html.parser')
    trs = soup.find_all('tr')
    #获取单个代理信息
    for tr in trs:
        #只保留高匿代理
        if tr.find_all(text='高匿'):
            IPinfo = tr.find('td',attrs={'class':'ip'}).find_all(['span','div'])
            item = [a.text for a in IPinfo]
            IP = ''.join(item[:-1])
            hTtp = tr.text.split('\n')[3]

            if IP not in proxydic:
                proxydic.update({IP+':'+item[-1]:hTtp.split(',')})

def proxy_xcdl(url,proxydic):
    soup = BeautifulSoup(gethtml(url), 'html.parser')
    trs = soup.find_all('tr',attrs={'class':'odd'})
    for tr in trs:
        if '高匿' in tr.text:
            detail = tr.text.split('\n')
            detail = [a for a in detail if a != '']
            #判断IP是否已有
            if detail[0] not in proxydic:
                proxydic.update({detail[0]+':'+detail[1]:detail[4].split(',')})

def proxy_test(n,ip,proxydic):
    proxies = {proxydic[ip][0]:'http://'+ip}
    try:
        resp = requests.get("http://www.baidu.com", proxies=proxies,timeout = 200)
        if resp.status_code == 200:
            return ip
    except:
        pass
    n += 1
    print("\r当前进度: {:.2f}%".format(n * 100 / len(proxydic)), end="")


def proxy_save(item,proxydic):
    jsonroot = 'D:/study/proxy/'
    if not os.path.isdir(jsonroot):
        os.mkdir(jsonroot)
    with open(jsonroot+'proxy.json','a') as f:
        f.write(json.dumps({item:proxydic[item][0]}))
        f.close()

getproxy()
prin('over thanks')