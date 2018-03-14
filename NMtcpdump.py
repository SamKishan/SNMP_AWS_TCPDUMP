import sys
import time
import re
import binascii
from scapy.all import *
scapy_cap=rdpcap("Lab5_Obj2_5.pcap")
i=0
length=len(scapy_cap)
ipv6_list=[]
for i in range(length):
    try:
        a=scapy_cap[i]['IPv6'].src
        #print(a)
        if a not in ipv6_list and a!="2001:1111:2222:7777::4":
            ipv6_list.append(a)
        
    except IndexError:
        #print("Continuing in spite of error")
        continue

mac6_list=[]
#Let's split the IPv6 addresses
for i in range(len(ipv6_list)):
    k=0
    for m in re.finditer(":",ipv6_list[i]):
        k=k+1
        if k==4:
            pos=m.start()
            mac6_list.append(ipv6_list[i][pos+1:])
            break
        
new_mac6_list=[]
for i in range(len(mac6_list)):
    a=mac6_list[i][1]            
    bin_str=bin(int(a,16))
    bin_str=str(bin_str)
    new_bin=bin_str[2:4]
    if(bin_str[4]=='0'):
        new_bin+='1'
    else:
        new_bin+='0'
    new_bin+=bin_str[5]
    #print("The hexadecimal is:"+str(hex(int(new_bin,2))))
    a=str(hex(int(new_bin,2)))
    a=a[2:]
    new_mac6_list.append(mac6_list[i][0])
    new_mac6_list[i]+=a
    new_mac6_list[i]+=mac6_list[i][2:]
    new_mac6_list[i]=new_mac6_list[i].replace("ff:fe",'')
print("The MAC addresses are:")
print(new_mac6_list)
sys.exit()
