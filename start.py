#!/usr/bin/env python3


import json
import time
import smtplib
from mygoodwe import Goodwe
from globals import *


def send_mail(msg):
	subject = 'MY SEMS INFO'
	body = 'Automation info from my sems: \n\n %s' % msg

	email_text = """\
		From: %s
		To: %s
		Subject: %s

		%s
	""" % (MAIL_FROM, MAIL_TO, subject, body)


	try:
	        server = smtplib.SMTP('smtp.gmail.com', 587)
	        server.ehlo()
	        server.starttls()
	        server.login(MAIL_USERNAME, MAIL_PASSWORD)
	        server.sendmail(MAIL_FROM, MAIL_TO, email_text)
	        server.quit()
	except:
		print('send email error')


def my_avg(my_dict):
	return round(sum(my_dict) / len(my_dict),0)

#params id,username,password
gw = Goodwe(SEMS_ID,SEMS_USR,SEMS_PWD)

dict_pv = []
dict_load = []
dict_bat = []
dict_grid = []

#send_mail("test \r\n ")

running = True
while running:
	gw.call()
	dict_data = gw.get_dict_data();
	pv_len = len(dict_pv)
	if pv_len > 5  :
		dict_pv.pop(0)
		dict_load.pop(0)
		dict_bat.pop(0)
		dict_grid.pop(0)

	dict_pv.append(dict_data['pv'])
	dict_load.append(dict_data['load'])
	dict_bat.append(dict_data['battery'])
	dict_grid.append(dict_data['grid'])
	str_out = "AVG PV:%d | AVG LOAD:%d | AVG BAT:%d | AVG GRID:%d | SOC %d" % (my_avg(dict_pv),my_avg(dict_load),my_avg(dict_bat),my_avg(dict_grid),dict_data['soc'])
	print(str_out)
	print(dict_data['bat_sta'])
	print("--------------------------------------------------------------------")
	if my_avg(dict_bat) > 2000 and dict_data['bat_sta'] == 3 :
		send_mail("SEMS INFO \r\n %s" %str_out)
	time.sleep(60)


