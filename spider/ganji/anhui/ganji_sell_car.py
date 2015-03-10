# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import socket 
#socket.setdefaulttimeout(30) 
import re
import MySQLdb
import threading
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,WebDriverException
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup



import os
from PIL import Image,ImageFilter,ImageEnhance
from StringIO import StringIO
import pytesseract

def grabHref(url,localfile):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
    html = None
    fails = 0
    while True:
        try:
            if fails >= 10: 
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    if html is not None:
        dictionary = {}
        content = BeautifulSoup(html).find_all('a')
        pat = re.compile(r'http://\w+.ganji.com/ershouche/\d+x.htm')
        for item in content:
             href = pat.findall(str(item))
             if href:
                 #if href[0] not in dictionary:
                     if len(str(href[0]).split('/'))>2 and len(str(href[0]).split('/')[2].split('.'))>0:
                         #if str(href[0]).split('/')[2].split('.')[0] == 'changzhou':
                             #dictionary[href[0]] = ''
                             print "====================================================================================================================================="
                             print href[0]
                             get_qiugou_info(href[0])
                             print "======================================================================================================================================"

def get_telephone(img_src):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(img_src,headers=heads)
    fails = 0
    while True:
        try:
            if fails >= 10:
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    file1 = StringIO(html)
    img = Image.open(file1)
    vcode = pytesseract.image_to_string(img)
    return vcode


def get_qiugou_info(myUrl):
    #proxy = {'http':'http://202.106.16.36:3128'}
    #proxy_support = urllib2.ProxyHandler(proxy)
    #opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
    #urllib2.install_opener(opener)  
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(myUrl,headers=heads)
    html = ''
    fails = 0
    while True:
        try:
            if fails >= 10: 
                break
            response = urllib2.urlopen(req,timeout=30)
            html = response.read()
        except:
            fails += 1
            print "Handing brand,the network may be not Ok,please wait...",fails
        else:
            break
    if html != '':
        soup = BeautifulSoup(html)
        title = ''
        prices = ''
        

        if myUrl.split('/')[2].split('.')[0] == 'hf':
            addrs = u'安徽合肥'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'wuhu':
            addrs = u'安徽芜湖'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'bengbu':
            addrs = u'安徽蚌埠'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'maanshan':
            addrs = u'安徽马鞍山'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'anqing':
            addrs = u'安徽安庆'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'chuzhou':
            addrs = u'安徽滁州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'fuyang':
            addrs = u'安徽阜阳'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'ahsuzhou':
            addrs = u'安徽宿州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'chaohu':
            addrs = u'安徽巢湖'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'luan':
            addrs = u'安徽六安'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'huainan':
            addrs = u'安徽淮南'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'huaibei':
            addrs = u'安徽淮北'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'tongling':
            addrs = u'安徽铜陵'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'huangshan':
            addrs = u'安徽黄山'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'bozhou':
            addrs = u'安徽亳州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'chizhou':
            addrs = u'安徽池州'.encode('utf-8')
        elif myUrl.split('/')[2].split('.')[0] == 'xuancheng':
            addrs = u'安徽宣城'.encode('utf-8')
        else:
            addrs = None
        name = ''
        brand_model = ''
        release_time = ''
        telephone = ''
        trip_distance = ''
        licenses = ''
 
        current_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        j = 1
        for h1 in soup.find_all('h1',attrs={'class':'title-name'}):
            title = str(h1.get_text()).replace('\n','')
        for ul in soup.find_all('ul',attrs={'class':'title-info-l clearfix'}):
            for i in ul.find_all('i',attrs={'class':'f10 pr-5'}):
                release_time = '2015-' + str(i.get_text())
        for div in soup.find_all('div',attrs={'class':'basic-info'}):
            for ul in div.find_all('ul',attrs={'class':'veh-plbit-ul clearfix'}):
                for li in ul.find_all('li'):
                    for i in li.find_all('i',attrs={'class':'comNum ft30'}):
                        prices = str(i.get_text())
                    for span in li.find_all('span',attrs={'class':'fc-999 dettips ft-12'}):
                        prices += str(span.get_text()).replace('\n','').replace(' ','')
                    
                    if j == 2:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            brand_model = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                    elif j == 3:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            trip_distance = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                    elif j == 4:
                        if len(str(li.get_text()).replace('\n','').replace(' ','').split('：'))>1:
                            licenses = str(li.get_text()).replace('\n','').replace(' ','').split('：')[1]
                     
                    j += 1
            for span in div.find_all('span',attrs={'name':'img-phone','class':'telephone'}):
                telephone += str(span.get_text()).replace('\n','').replace(' ','') + ','
                for img in span.find_all('img'):
                    telephone = 'http://' + myUrl.split('/')[2].split('.')[0] + '.ganji.com' + str(img.get('src'))
            for li in div.find_all('li',attrs={'class':'fl'}):
                if len(str(li.get_text()).split('\n'))>1:
                    name = str(li.get_text()).split('\n')[1].replace(' ','')
        #print telephone.rstrip(',')
        #print name   
        #print title,release_time,telephone.rstrip(','),name,prices,brand_model,trip_distance,licenses,myUrl
        if telephone != '':
            #if telephone.startswith("http"):
            #    try:
            #        telephone = get_telephone(telephone)
            #    except:
            #        print "telephone number convert failed..."
            print title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl
            #res = [title,release_time,telephone.rstrip(','),name,addrs,prices,brand_model,trip_distance,licenses,myUrl]
            try:
                conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
                curs = conn.cursor()
                conn.select_db('spider')
                curs.execute("select id from sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                is_seller=u'个人'.encode('utf-8')
                if not getrows:
                    curs.execute("select id from sell_car_info where telephone_num='%s'" % telephone.rstrip(','))
                    get_telephones = curs.fetchall()
                    if not get_telephones:
                        is_seller=u'个人'.encode('utf-8')
                    else:
                        is_seller=u'商家'.encode('utf-8')
                    if telephone.startswith("400"):
                        is_seller=u'商家'.encode('utf-8')
                    car_config = brand_model + " | " + trip_distance + " | " + licenses
                    info_src = "ganji"
                    res = [title,car_config,name,telephone.rstrip(','),addrs,release_time,prices,is_seller,info_src,myUrl]
                    print "The data is not exists in the database..."
                    curs.execute("insert into sell_car_info(title,car_config,name,telephone_num,addrs,release_time,prices,is_seller,info_src,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
                conn.commit()
                curs.close()
                conn.close()
            except MySQLdb.Error,e:
                print "Error %d %s" % (e.args[0],e.args[1])
                sys.exit(1)

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1345408840x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1305811548x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1318837868x.htm')


#print "=================================================================================="

##get_qiugou_info('http://maanshan.ganji.com/ershouche/1339247794x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1338944828x.htm')

#print "=================================================================================="

#get_qiugou_info('http://nj.ganji.com/ershouche/1336617045x.htm')




def main():
    addr_list = ['hf','wuhu','bengbu','maanshan','anqing','chuzhou','fuyang','ahsuzhou','chaohu','luan','huainan','huaibei','tongling','huangshan','bozhou','chizhou','xuancheng']
    for j in range(len(addr_list)):
        url = "http://" + addr_list[j] + ".ganji.com/ershouche/a1o"
        localfile="Href.txt"
        for i in range(1,4):
            print "current page is %d" % i
            myUrl = url + str(i)
            t = threading.Thread(target=grabHref(myUrl,localfile))
            t.start()
            print "current page is %d" % i

if __name__=="__main__":
    main()
