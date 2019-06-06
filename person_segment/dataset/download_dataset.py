import re
import wget
import os

# Dependencies:
# $ sudo pip3 install python3-wget

fn="./alldata_urls.txt"
roifn="./crop.txt"

read_data = None
with open(fn) as f:
	read_data = f.read()
	#print(read_data)
f.close()

fn_list=re.split(' |\n',read_data)

fn_num = len(fn_list) - 1
print("filen number = ", fn_num)

idx_list = []
for i in range( fn_num ):
	idx_list.append(i)

# Check result save path
dst_path="./images/"
if not os.path.exists(dst_path):
	os.mkdir(dst_path)

# loop download
# it = iter(idx_list)
# for x, y in zip(it, it):
#     if fn_list[y] == 'None':
#     	print(fn_list[x], " == ", fn_list[y])
#     	continue
#     else:
#     	print("Donwload:", fn_list[y])
#     	wget.download(fn_list[y], dst_path + fn_list[x])

# Multiple threads download
import os
import requests
from time import time
from multiprocessing import Pool

def url_response(param):
	global fn_list
	print(param)
	[x, y] = param

	if fn_list[y] == 'None':
		print(fn_list[x], " == ", fn_list[y])
	else:
		print("Donwload:", fn_list[y])
		myfile = requests.get(fn_list[y])
		open(dst_path + fn_list[x], 'wb').write(myfile.content)

it = iter(idx_list)
arr_multiple_param=[]
for x, y in zip(it, it):
	arr_multiple_param.append([x, y])

with Pool(20) as p:
	p.map(url_response, arr_multiple_param)

print("Download finish")