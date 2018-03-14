import sys 
try:
    from prettytable import PrettyTable
    import boto3
    import pytz
    import json
    from time import gmtime, strftime
    from datetime import datetime, date, time, timedelta
    from dateutil import parser
    import sys
except ImportError:
    print("Missing one or more modules. Check the source code to find out what modules need to be installed")
    print("program exiting")
    sys.exit()
try:
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket='netman-lab5-saki8093', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
except:
    print("Bucket already created")

x=PrettyTable()
x.field_names=["File name","Status",]
s3=boto3.resource('s3')
data_1=open("statistics.txt")
data_2=open("CPU_utilization_R1.png")

file_name_1="statistics"+str(strftime("_%Y-%m-%d_%H:%M:%S", gmtime()))+".txt"
object=s3.Object('netman-lab5-saki8093',file_name_1)
file_name_2="CPU_stats"+str(strftime("_%Y-%m-%d_%H:%M:%S", gmtime()))+".png"
object.put(Body=data_1)
object_2=s3.Object('netman-lab5-saki8093',file_name_2)
object_2.put(Body=data_2)
client = boto3.client('s3')
keys=client.list_objects(Bucket='netman-lab5-saki8093')
delete=[]
i=1
for key in keys['Contents']:
    now=datetime.utcnow().replace(tzinfo=pytz.timezone('GMT'))
    if (now - key['LastModified']  >  timedelta(minutes=3)):
        x.add_row([key['Key'],"Deleted"])
        delete.append(key['Key'])
    else:
        x.add_row([key['Key'],"Alive"])

for i in range(len(delete)):
    client.delete_object(Bucket='netman-lab5-saki8093', Key=delete[i])
print(" Status of objects in the bucket")
print(x)
sys.exit()
