#!/usr/bin/env python3


import json
import time
import smtplib
from mygoodwe import Goodwe
from globals import *

bat_stat_txt = { 0 : 'Non', 1 : '?', 2 : 'Discharging', 3 : 'Charging'}
bat_mail = 1
soc_mail = 1
dict_pv = []
dict_load = []
dict_bat = []
dict_grid = []

# send email 
# param mail text
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


#create instance of goodwe object
gw = Goodwe(SEMS_ID,SEMS_USR,SEMS_PWD)

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
		bat_mail = 1

	dict_pv.append(dict_data['pv'])
	dict_load.append(dict_data['load'])
	dict_grid.append(dict_data['grid'])
	str_out = "AVG PV:%d | AVG LOAD:%d | AVG BAT:%d | AVG GRID:%d | SOC %d  %s" % (my_avg(dict_pv),my_avg(dict_load),my_avg(dict_bat),my_avg(dict_grid),dict_data['soc'],bat_stat_txt[dict_data['bat_sta']])
#	print(str_out)
	print(dict_bat)
	print("--------------------------------------------------------------------")
	if my_avg(dict_bat) > 2000 and dict_data['bat_sta'] == 3 and bat_mail > 0:
		send_mail("SEMS INFO \r\n %s" %str_out)
		bat_mail = 0

	if dict_data['soc'] == 70 and soc_mail > 0:
                send_mail("SEMS INFO Battery 70% \r\n %s" %str_out)
                soc_mail = 0

	time.sleep(60)
