# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib
import urllib2
import re
import MySQLdb
import pytesseract
from PIL import Image
from cStringIO import StringIO
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from bs4 import BeautifulSoup
import socket 
#socket.setdefaulttimeout(30) 

def grabHref(url,localfile,address):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':user_agent}
    req = urllib2.Request(url,headers=heads)
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
    for div in BeautifulSoup(html).find_all("div",attrs={'class':'tc14-cary-list haoctuij'}):
        content = div.find_all('a')
    pat = re.compile(r'http://www.taoche.com/buycar/[bp]-[A-Za-z0-9]+.html')
    dictionary = {}
    for item in content:
        href = pat.findall(str(item))
        if href:
            #if href[0] not in dictionary:
                #dictionary[href[0]] = ''
                print href[0]
                get_qiugou_info(href[0],address)



def get_qiugou_info(myUrl,address):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    heads = {'User-Agent':'Mozilla/5.0'}
    req = urllib2.Request(myUrl,headers=heads)
    html = ''
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
        for div in soup.find_all('div',attrs={'class':'tc14-cyxq-tit'}):
            for tit in div.find_all('h3'):
                if address not in str(tit.get_text()):
                    title = address + str(tit.get_text()).replace(' ','').replace('\n','')
                else:
                    title = str(tit.get_text()).replace(' ','').replace('\n','')
    #title = soup.find_all('h3')
        print title
        vehicle_series = ''
        prices = ''
        vehicle_class = ''
        vehicle_age = ''
        vehicle_color = ''
        addr = ''
        name = ''
        release_time = ''
        img_src = ''
        other_requirements = ''
        mileage = ''
        license = ''
        highlights = ''
        contact = u'联系人'.encode('utf-8')
        is_seller = ''
        seller_readme = ''
        i = 1
        j = 1
        for ul in soup.find_all("ul",attrs={'class':'tc14-cyjglist'}):
            for li in ul.find_all("li",attrs={'class':'first'}):
                for em in li.find("em"):
                    prices = str(em).replace(' ','').replace('\n','')
            for li in ul.find_all("li"):
                if li not in ul.find_all("li",attrs={'class':'first'}):
                    if i == 1:
                        mileage = str(li.get_text()).replace(' ','').split('：')[1].replace('\n','')
                    elif i == 2:
                        license = str(li.get_text()).replace(' ','').split('：')[1].replace('\n','')
                    elif i == 3:
                        highlights = str(li.get_text()).replace(' ','').split('：')[1].replace('\n','')
                    i += 1
        for div in soup.find_all("div",attrs={'class':'tc14-cydh'}):
            img_src = str(div.get('style'))[str(div.get('style')).find('htt'):-2]
        for div in soup.find_all("div",attrs={'class':'tc14-cyhpon','id':'divParaTel'}):
            for p in div.find_all("p"):
                if j == 1:
                    is_seller = str(p.get_text()).replace(' ','').replace('\n','')
                elif j == 2:
                    name = str(p.get_text()).replace(' ','').replace('\n','')
                j += 1
        for p in soup.find_all("p",attrs={'class':'chyxx_text'}):
            seller_readme += str(p.get_text())
        for div in soup.find_all("div",attrs={'class':'tc14-tabtitbox tc14-tab-h53  tc14-cytab clearfix'}):
            for span in div.find_all("span"):
                if len(str(span.get_text()))>=2:
                    release_time = str(span.get_text()).split(' ')[-2]  
    #print prices,mileage,license,highlights,img_src,is_seller,name,release_time,myUrl
    #print seller_readme
        if img_src != '':
            print 'This car info is useful...'
        else:
            print 'This car is selled already..'
        telephone_num = ''
        if img_src != '':
            try:
                telephone_num = get_telephone(img_src)
            except:
                print "convert telephone failed..."
        #res = [title,name,release_time,is_seller,prices,mileage,license,highlights,img_src,seller_readme,myUrl]
        uni_number = str(myUrl.split('/')[-1]).split('.')[0]
        is_seller = u'商家'.encode('utf-8')
        #if img_src.find('ttp')>0:
        #    urllib.urlretrieve(img_src,'/data/python/spider/yiche/telephone_img_sell_car/%s.jpg' % uni_number)
        try:
            conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='dp')
            curs = conn.cursor()
            conn.select_db('spider')
            if img_src != '':
                curs.execute("select id from yiche_sell_car_info where url='%s'" % myUrl)
                getrows=curs.fetchall()
                if not getrows:
                    res = [title,name,telephone_num,release_time,is_seller,prices,mileage,license,highlights,img_src,seller_readme,myUrl]
                    curs.execute("insert into yiche_sell_car_info(title,name,telephone_num,release_time,is_seller,prices,mileage,license,highlights,img_src,seller_readme,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",res)
                else:
                    print 'The data is already in the database...'
            conn.commit()
            curs.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Error %d %s" % (e.args[0],e.args[1])
            sys.exit(1)


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


#get_qiugou_info('http://www.taoche.com/buycar/b-DealerAUDI1089278S.html')

#print "================seller===================="
#get_qiugou_info('http://www.taoche.com/buycar/b-Dealer14120412153.html')


#print "================single===================="
#get_qiugou_info('http://www.taoche.com/buycar/p-5315995.html')

#get_qiugou_info('http://www.taoche.com/buycar/b-DealerAUDI1087451S.html')
#get_qiugou_info('http://www.taoche.com/buycar/b-Dealer15011410446.html')
def main():
    url_list = ["http://jiangsu.taoche.com/buycar/pges2bxcdza/?page=","http://shanghai.taoche.com/buycar/pges2bxcdza/?page=","http://zhejiang.taoche.com/buycar/pges2bxcdza/?page=","http://shandong.taoche.com/buycar/pges2bxcdza/?page=","http://anhui.taoche.com/buycar/pges2bxcdza/?page="]
    for url in url_list:
        address = ''
        if url.split('/')[2].split('.')[0]=="jiangsu":
            address=u'江苏'.encode('utf-8')
        elif url.split('/')[2].split('.')[0]=="shandong"
            address=u'山东'.encode('utf-8')
        elif url.split('/')[2].split('.')[0]=="shanghai"
            address=u'上海'.encode('utf-8')
        elif url.split('/')[2].split('.')[0]=="zhejiang"
            address=u'浙江'.encode('utf-8')
        elif url.split('/')[2].split('.')[0]=="anhui"
            address=u'安徽'.encode('utf-8')
        localfile="Href.txt"
        for i in range(1,30):
            myUrl = url + str(i)
            grabHref(myUrl,localfile,address)

if __name__=="__main__":
    main()
