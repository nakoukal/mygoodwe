#!/usr/bin/env python3


import json
import time
from mygoodwe import Goodwe

#params id,username,password
gw = Goodwe('fbe32e72-d111-42b9-ac0f-bac5a66d30dd','radek@nakoukal.com','RadFre1977Goodwe')



running = True
while running:
	gw.call()
	print('json')
	print(gw.get_json_data())
	print('formated output')
	gw.show()
	print("---------------------------")
	time.sleep(60)
