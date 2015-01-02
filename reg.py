import cookielib,urllib,urllib2
from bs4 import BeautifulSoup

def ifel(a,b,c):
	if(a==True):
		return(b)
	else:
		return(c)

print('Dining Register')
name=raw_input("SID:  ") ##change to "'115501xxxxx'" (include')
password=raw_input("password:  ") ##change to "'xxxxxxxx'" (include')

url="https://cloud.itsc.cuhk.edu.hk//wrs/public/login.aspx?AppID=23"
url1="https://cloud.itsc.cuhk.edu.hk/wrs/WRSEvent.aspx"
url2="https://cloud.itsc.cuhk.edu.hk/wrs/WRSEventDetails.aspx"
url3="https://cloud.itsc.cuhk.edu.hk/wrs/WRSUserInfo.aspx"
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def para_login(soup,name,password):
	viewstate = soup.select("#__VIEWSTATE")[0]['value']
	eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
	viewstate_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
	return((
		('__EVENTARGUMENT',''),
		('__EVENTTARGET',''),
		('__EVENTVALIDATION',eventvalidation),
		('__VIEWSTATE',viewstate),
		('__VIEWSTATEGENERATOR',viewstate_generator),
		('btnSubmit','Login'),
		('txtLoginName',name),
		('txtPassword',password)
	))


def para_page(page,eventvalidation,viewstate,viewstate_generator):
	return((
		('ctl00_ScriptManager1_HiddenField','	;;AjaxControlToolkit, Version=4.1.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:acfc7575-cdee-46af-964f-5d85d9cdcf92:effe2a26:7dd386e9'),
		('__EVENTTARGET','ctl00$ContentPlaceHolder1$gvEventList'),
		('__EVENTARGUMENT','Page$'+str(page)),
		('__EVENTVALIDATION',eventvalidation),
		('__VIEWSTATE',viewstate),
		('__VIEWSTATEGENERATOR',viewstate_generator),
	))


def para_detail(num,eventvalidation,viewstate,viewstate_generator):
	return((
		('ctl00_ScriptManager1_HiddenField',';;AjaxControlToolkit, Version=4.1.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:acfc7575-cdee-46af-964f-5d85d9cdcf92:effe2a26:7dd386e9'),
		('__EVENTARGUMENT',''),
		('__EVENTTARGET','ctl00$ContentPlaceHolder1$gvEventList$ctl'+ifel(num<10,'0'+str(num),str(num))+'$lnkWorkshop'),
		('__EVENTVALIDATION',eventvalidation),
		('__VIEWSTATE',viewstate),
		('__VIEWSTATEGENERATOR',viewstate_generator),
	))


def para_info(eventvalidation,viewstate,viewstate_generator):
	return((
		('ctl00_ScriptManager1_HiddenField',';;AjaxControlToolkit, Version=4.1.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:acfc7575-cdee-46af-964f-5d85d9cdcf92:effe2a26:7dd386e9'),
		('__EVENTARGUMENT',''),
		('__EVENTTARGET',''),
		('__EVENTVALIDATION',eventvalidation),
		('__VIEWSTATE',viewstate),
		('__VIEWSTATEGENERATOR',viewstate_generator),
		('ctl00$ContentPlaceHolder1$btnRegister','Register this class')
	))


def para_result(eventvalidation,viewstate,viewstate_generator):
	return((
		('ctl00_ScriptManager1_HiddenField',';;AjaxControlToolkit, Version=4.1.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:acfc7575-cdee-46af-964f-5d85d9cdcf92:effe2a26:7dd386e9'),
		('__EVENTARGUMENT',''),
		('__EVENTTARGET',''),
		('__EVENTVALIDATION',eventvalidation),
		('__VIEWSTATE',viewstate),
		('__VIEWSTATEGENERATOR',viewstate_generator),
		('ctl00$ContentPlaceHolder1$txtUserName','bbq'),
		('ctl00$ContentPlaceHolder1$txtUserTel1','12345678'),
		('ctl00$ContentPlaceHolder1$txtUserTel2','87654321'),
		('ctl00$ContentPlaceHolder1$txtUserEmail','123456789@qq.com'),
		('ctl00$ContentPlaceHolder1$btnNext','Register')
	))
	

def read_login(url):
	f=urllib.urlopen(url)
	soup=BeautifulSoup(f)
	login_data=urllib.urlencode(para_login(soup,name,password))
	req=urllib2.Request(url)
	resp=opener.open(req,login_data)
	pageContent=resp.read()
	a=pageContent.find("Workshop Registration System - Available Events")
	if(a==-1):
		print("Invalid SID/password!")
		read_login(url)
	else:
		print("Login succeed!")
		return(BeautifulSoup(pageContent))


def read_one(i,eventvalidation,viewstate,viewstate_generator):
	req=urllib2.Request(url1)
	para=para_detail(i,eventvalidation,viewstate,viewstate_generator)
	login_data=urllib.urlencode(para)
	resp=opener.open(req,login_data)
	pageContent=resp.read()
	if(pageContent.find("You have already registered this class.")!=-1):
		print(''+str(i-1)+'th event has already been registered!')
	else:
		print('registering '+str(i-1)+'th event...')
		soup=BeautifulSoup(pageContent)
		viewstate = soup.select("#__VIEWSTATE")[0]['value']
		eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
		viewstate_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
		req=urllib2.Request(url2)
		para=para_info(eventvalidation,viewstate,viewstate_generator)
		login_data=urllib.urlencode(para)
		resp=opener.open(req,login_data)
		pageContent=resp.read()
		soup=BeautifulSoup(pageContent)
		viewstate = soup.select("#__VIEWSTATE")[0]['value']
		eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
		viewstate_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
		req=urllib2.Request(url3)
		para=para_result(eventvalidation,viewstate,viewstate_generator)
		login_data=urllib.urlencode(para)
		resp=opener.open(req,login_data)
		print('     registered!')


def read_page(page,soup):
	print('==========\nPage '+str(page))
	table=soup.find(id='ctl00_ContentPlaceHolder1_gvEventList')
	tr=table.findAll('tr')
	num=len(tr)-2
	viewstate = soup.select("#__VIEWSTATE")[0]['value']
	eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
	viewstate_generator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
	for i in range(2,num+1):
		read_one(i,eventvalidation,viewstate,viewstate_generator)
	if(num==11):
		page+=1
		req=urllib2.Request(url1)
		para=para_page(page,eventvalidation,viewstate,viewstate_generator)
		login_data=urllib.urlencode(para)
		resp=opener.open(req,login_data)
		pageContent=resp.read()
		soup=BeautifulSoup(pageContent)
		read_page(page,soup)


read_page(1,read_login(url))
print('==========\nfinished!')