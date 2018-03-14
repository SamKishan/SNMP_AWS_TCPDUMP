try:
    from easysnmp import Session 
    from prettytable import PrettyTable
    from time import gmtime, strftime
    import time 
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    import unicodedata
except:
    print("Missing one or more modules. Check the source code to determine which module you are missing and install it.")
    print("Program exiting")
    sys.exit()

k=["11","22","33","44","55"]
indic_list=[]
indices={}
final_dict={}
grand_dict={}
f2_dict={}
final2_dict={}
final3_dict={}
x=PrettyTable()
x.field_names=["Router","Interface","IPv4 address","MAC address"]
new_grand={}
outer={}
inner={}
for i in range(len(k)):
    session=Session(hostname="198.51.100."+str(k[i]), community="public", version=2,  use_sprint_value=True)
    ip_addr=session.walk('.1.3.6.1.2.1.4.20.1.2')
    des=session.walk('ifName')
    mac=session.walk("ifPhysAddress")
    hostname=session.get('sysName.0')
    #start=hostname.find("value=\'")
    #end=hostname.find(" (oid=")
    print("Hostname: "+str(hostname.value))
    print("len of ip_addr: "+str(len(ip_addr)))
    #print("Mac stuff for "+str(hostname.value)+"\n")
    #print(str(mac))
    for i in range(len(ip_addr)):
        print("description: "+str(des[i].oid_index)+"  "+str(des[i].value))
        print("IP addr: "+str(ip_addr[i].value)+"  "+str(ip_addr[i].oid_index))
        print("MAC addr: "+str(mac[i].oid_index)+"  "+str(mac[i].value))
        print("\n\n")
        inner["IP address"]=str(ip_addr[i].oid_index)
        inner["MAC address"]=str(mac[i].value)
        outer[str(des[i].value)]=inner
        inner={}        
    new_grand[str(hostname.value)]=outer
    outer={}
print("Final grand dictionary")
for key in new_grand.keys():
    print(str(key)+"   "+str(new_grand[key]))




grand_int_status={}
a={}
b={}
mix={}
for i in range(len(k)):
    session=Session(hostname="198.51.100."+str(k[i]), community="public", version=2)
    status=session.walk("ifAdminStatus")
    hostname=str(session.get('sysName.0'))
    start=hostname.find("value=\'")
    end=hostname.find(" (oid=")
    #print("Interface status and index")
    for item in status:
        if(item.oid_index!="5"):
            #print(str(item.value+"   "+item.oid_index))
            a[item.oid_index]=item.value
    if_name=session.walk("ifName")
    print("\n")
    #print("Interface name and index")
    for if_item in if_name:
        if(if_item.oid_index!="5"):
            #print(str(if_item.value+"   "+if_item.oid_index))
            b[if_item.oid_index]=if_item.value
    #print(if_name)
    for key in a.keys():
        b_key=unicodedata.normalize('NFKD', b[key]).encode('ascii','ignore')
        a_key=unicodedata.normalize('NFKD', a[key]).encode('ascii','ignore')
        if(a_key=="1"):
            a_key="Up"
        elif(a_key=="2"):
            a_key="Down"
        mix[b_key]=a_key
    print("Status of :"+hostname[start+7:end-1])
    host_name=hostname[start+7:end-1]
    grand_int_status[host_name]=mix
    print(mix)
    mix={}
print("The grand status dictionary")
print(grand_int_status)




f=open("statistics.txt","w")
f.write("{ \n")
for key in new_grand.keys():
    value=new_grand[key]
    f.write("\n\t "+key+":{")
    for key_2 in new_grand[key].keys():
        f.write("\n\t\t "+str(key_2)+" { \n")
        f.write("\t\t\t"+str(new_grand[key][key_2]))
        #f.write("\t\t\t"+str(new_grand[key]['MAC address']))
        f.write("\n\t\t }")
    f.write("\n\t }")
f.write("\n}\n")

f.write("\n\n\n")
f.write("Interface status: \n\n")
f.write("{ \n")
for key in grand_int_status.keys():
    value=grand_int_status[key]
    f.write("\n\t "+key+":{")
    for key_2 in grand_int_status[key].keys():
        f.write("\n\t\t"+key_2+" : "+grand_int_status[key][key_2])
    f.write("\n\t } ")
f.write("\n }")

#f.write(str(grand_int_status))
f.close()


ses_R1 = Session(hostname='198.51.100.11', community='public', version=2)
#print("Time: "+ str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
CPU_percent=[]
x_axis=[]
for i in range(0,30):
    CPU_ut=ses_R1.walk(".1.3.6.1.4.1.9.2.1.56")
    print("CPU utilization (%) at the "+str(i*5)+"th second")
    for item in CPU_ut:
        print(str(item.value))
        CPU_percent.append(int(item.value))
        x_axis.append(i*5)
    time.sleep(5)

plt.ylabel("CPU utilization (%)")
print("x_axis: "+str(x_axis))
x=[]
for i in range(len(x_axis)):
    x.append(i)
x_2=np.array(x)
plt.xticks(x,x_axis)
plt.title('CPU utilization(%) of R1 over 5 minutes with 5 second intervals')
plt.xlabel(" Time (s)")
plt.plot(CPU_percent)
fig=plt.gcf()
fig.savefig("CPU_utilization_R1.png")
plt.show()
plt.gcf().clear()
sys.exit()

