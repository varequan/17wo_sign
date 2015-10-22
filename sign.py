#! /usr/bin/env python
#coding:utf-8
 
import sys
import re
import urllib2
import urllib
import requests
import cookielib
import time
import datetime
import json
## 这段代码是用于解决中文报错的问题  
reload(sys)  
sys.setdefaultencoding("utf8")  
#####################################################
#登录17wo

loginurl ="http://17wo.cn/Login!process.action"


#http://17wo.cn/SignIn!share.action?sharecontent=abc&_=1445312483524

#http://17wo.cn/SignIn!playEggLuckDraw.action?_=1445311617422
#http://17wo.cn/SignIn!share.action?sharecontent=abc&_=1445311688051
#
#http://17wo.cn/FlowRedPacket!LuckDraw.action?pageName=&_=1445311829219
#http://17wo.cn/FlowRedPacket!share.action?sendid=&sharecontent=undefined&subjectId=0&cpd=&_=1445311946704
#
#http://17wo.cn/UserCenterGrowup!gainTaskAwards.action?aId=117&taskId=28&_=1445312373615
#http://17wo.cn/UserCenterGrowup!share.action?sharecontent=hello&_=1445312414709
#
#http://17wo.cn/UserCenterGrowup!gainTaskAwards.action?aId=117&taskId=29&_=1445312187398
#http://17wo.cn/UserCenterGrowup!share.action?sharecontent=hello&_=1445312223579
#顺序：1）签到
#	  2）分享
#	  3）红包
#	  4）分享
logindomain = '17wo.cn'
 
class sign17wo(object):
     
    def __init__(self):
        self.phoneNumber = ''
        self.passwprd = ''
        self.domain = ''
 
        self.cj = cookielib.LWPCookieJar()            
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)) 
        urllib2.install_opener(self.opener)    
     
    def setLoginInfo(self,phoneNumber,password,domain):
        '''设置用户登录信息'''
        self.phoneNumber = phoneNumber
        self.pwd = password
        self.domain = domain
 
    def login(self):
        '''登录网站'''
        print str(self.phoneNumber)+" 正在登陆..."
        loginparams = {
        	"mobile":self.phoneNumber,
			"backurl":"",
			"backurl2":"",
			"password":self.pwd,
			"chk":"",
			"loginType":"0",
			"chkType":"on",
		}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams),headers=headers)  
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = response.read()      
        #print thePage

    def task(self,taskid):
        '''每日任务'''
        print "正在完成每日任务（任务id："+ str(taskid) +"）...",
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/UserCenterGrowup!gainTaskAwards.action?aId=117&taskId="+str(taskid)+"&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print thePage
        if s['success'] == True:
            print "得到"+s['data']['prize']
            if s['data']['share']:
                self.taskShare(taskid)
        else:
            print s['message']

    def taskShare(self,taskid):
        '''完成任务分享'''
        print "正在进行社交网站分享...",
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/UserCenterGrowup!share.action?sharecontent=hello&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print thePage
        if(s['success']==True):
            print "分享成功（任务id："+ str(taskid) +"）"
        else:
            print s["message"]
  
    def sign(self):
        '''每日签到'''
        print "正在签到..",
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/SignIn!checkin.action?checkIn=true&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print s['success']
        #print thePage
        if(s['success']==True):
            print s["message"]
            print "本次签到获得"+str(s['data']['giftFlow'])+"M"
            print "第"+str(s['data']['continousSignDay'])+"天签到，",
            print "连续签到"+str(s['data']['count'])+"天，",
            print "这个月签到"+str(s['data']['signMonthTotal'])+"天，",
            print "一起沃流量账户："+str(s['data']['flowrateNum'])+"M"

            if s['data']['continousSignDay'] == 3:
                print "获得一次砸金蛋奖励"
                self.signEgg()
            elif s['data']['continousSignDay'] == 7:
                pass
            self.signShare()
        else:
            print s["message"]

#http://17wo.cn/SignIn!playEggLuckDraw.action?_=1445401401627
    def signEgg(self):
    	'''砸蛋'''
    	plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/SignIn!playEggLuckDraw.action?_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print thePage
        if(s['success']==True):
            print s['data']['message']['prize']
        else:
            print s["message"]

    def signShare(self):
        '''完成签到分享'''
        print "正在进行社交网站分享...",
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/SignIn!share.action?sharecontent=abc&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print thePage
        if(s['success']==True):
            print "分享成功（签到）"
        else:
            print s["message"]
        
    def redPacket(self):
        '''红包'''
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/FlowRedPacket!LuckDraw.action?pageName=&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        print "流量红包：",
        #print thePage
        if(s['success']==True):
            if s['data']["message"]['awardType']<0:
                print s['data']["message"]['errMsg']
            else:
                print s['data']["message"]['info']
                self.redPacketShare()
        else:
            print s["message"]

    def redPacketShare(self):
        '''红包分享'''
        print "正在进行社交网站分享...",
        plt = long('%.0f' % (time.time() * 1000))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request("http://17wo.cn/FlowRedPacket!share.action?sendid=&sharecontent=undefined&subjectId=0&cpd=&_="+str(plt),headers=headers) 
        response = urllib2.urlopen(req)
        thePage = response.read()      
        s = json.loads(thePage)
        #print thePage
        if(s['success']==True):
            print "分享成功（红包）"
        else:
            print s["message"]

if __name__ == '__main__':   
    phones=[
    	{
    		"mobile":"130185*****",
    		"pw":"******",
    	},
    	{
    		"mobile":"185662*****",
    		"pw":"******",
    	},
    	{
    		"mobile":"132723*****",
    		"pw":"******",
    	}
    ]

    for i in range(len(phones)):
		sign = sign17wo()
		phoneNumber = phones[i]["mobile"]
		password = phones[i]["pw"]
		domain = logindomain
		sign.setLoginInfo(phoneNumber,password,domain)
		sign.login()
		sign.task(28)
		sign.sign()
		sign.redPacket()
		sign.task(29)
		print "==================================================="

