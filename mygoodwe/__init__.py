#!/usr/bin/env python3                                                                                                                                                                                                                                                                                                                                                                                                                                                                    import requests

import json
import logging
import requests
import time
from datetime import datetime

class  Goodwe:

	def __init__(self,id,acnt, passw):

		self.id = id
		self.usr = acnt
		self.pwd = passw
		self.token = json.dumps({"uid":id,"client":"web","version":"1.0","language":"en"})
		self.payload = {'powerStationId' :id}
		self.bat_stat_txt = { 0 : 'Non', 1 : '?', 2 : 'Discharging', 3 : 'Charging'}
		self.load_stat_txt = { 0 : 'Non', -1 : 'Importing', 1 : 'Using Battery' }
		self.solar = ""
		self.battery = ""
		self.bat_stat = ""
		self.load = ""
		self.load_stat = ""
		self.soc = ""
		self.grid = ""
		self.grid_stat = ""
		self.json_data = "{}"
		self.dict_data = {};

	def call(self):
		for i in range(1,4):
			try:
				headers={
					'Content-Type':'application/json;charset=UTF-8',
					'Accept':'application/json',
					'token':self.token
				}
#				print(self.token)
				r = requests.post('http://globalapi.sems.com.cn:82/api/v2/PowerStation/GetPowerflow',headers=headers, data=json.dumps(self.payload), timeout=20)
				r.raise_for_status()
				data = r.json();
				if data['msg'] == 'success' and data['data'] is not None:
#					print(data)
					res_data = data['data']
					self.json_data = res_data
					self.dict_data = {
						'pv': float(res_data['pv'][:-3]),
						'battery': float(res_data['bettery'][:-3]),
						'bat_sta': res_data['betteryStatus'],
						'load': float(res_data['load'][:-3]),
						'load_sta': res_data['loadStatus'],
						'soc': int(res_data['socText'][:-1]),
						'grid': float(res_data['grid'][:-3]),
						'grid_sta': res_data['gridStatus']		
					}
					self.json_data = res_data
					self.solar = res_data['pv']
					self.battery = res_data['bettery']
					self.bat_stat = "%s (%s)" % (res_data['betteryStatus'],self.bat_stat_txt[res_data['betteryStatus']])
					self.load = res_data['load']
					self.load_stat = "%s (%s)" % (res_data['loadStatus'], self.load_stat_txt[res_data['loadStatus']])
					self.soc = res_data['socText']
					self.grid = res_data['grid']
					self.grid_stat = res_data['gridStatus']
					return
				else:
					print("loging")
					login_payload = { 'account': self.usr, 'pwd': self.pwd }
					r = requests.post('http://globalapi.sems.com.cn:82/api/v2/Common/CrossLogin',headers=headers, data=json.dumps(login_payload), timeout=10)
					r.raise_for_status()
					data = r.json()
					self.token = json.dumps(data['data'])
			except requests.exceptions.RequestException as exp:
				print(exp)

			time.sleep(i ** 3)

	def get_dict_data(self):
		return self.dict_data;

	def show(self):
		print("solar  :",self.solar)
		print("battery:",self.battery)
		print("bat_sta:",self.bat_stat)
		print("load   :",self.load)
		print("load_st:",self.load_stat)
		print("soc    :",self.soc)
		print("grid   :",self.grid)
		print("grid_st:",self.grid_stat)

	def get_json_data(self):
		return self.json_data
