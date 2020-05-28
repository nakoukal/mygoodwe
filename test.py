#!/usr/bin/env python3


import json
import time
from mygoodwe import Goodwe
from globals import *

#params id,username,password
gw = Goodwe(SEMS_ID,SEMS_USR,SEMS_PWD)

running = True
while running:
	gw.call()
#	print('dict')
#	print(gw.get_dict_data())
	print('\n json')
	print(gw.get_json_data())
#	print('\n formated output')
#	gw.show()
	print("---------------------------")
	time.sleep(60)
