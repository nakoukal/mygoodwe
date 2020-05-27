#!/usr/bin/env python3


import json
import time
from mygoodwe import Goodwe

#params id,username,password
gw = Goodwe('goodwe id','username','password')
gw.call("true")
print(gw.get_json_data())



#running = True
#while running:
#	gw.call()
#	print('dict')
#	print(gw.get_dict_data())
#	print('json')
#	print(gw.get_json_data())
#	print('formated output')
#	gw.show()
#	print("---------------------------")
#	time.sleep(60)
