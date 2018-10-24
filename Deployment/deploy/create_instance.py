#Acknowledgement
#Acknowledge to this shell file developed by Team 18 of COMP90024 of The University of Melbourne, under Apache Licence(see LICENCE).


import time
import boto
from boto.ec2.regioninfo import RegionInfo
import json

'''
Create a instance and a "size" GB volumn, return the volumn
'''
def create(size):
    print ("Creating instance of",size,"GB")
    vol_req = conn.create_volume(
        size, region, volume_type=volumn_type)
    inst=conn.run_instances(
        image_name,
        key_name=key_pair,
        instance_type=instance_type,
        security_groups=sec_group,
        placement=region)

    print ("Created a", size ,"GB instance")
    return vol_req

'''
print the instance info from the list
'''
def print_instances(res):
    for ins in res:
        print ("---------------------")
        print ("IP: ", ins.instances[0].private_ip_address)
        print ("Placement: ", ins.instances[0].placement)
        print ("ID: ", ins.instances[0].id)
        print ("Key: ", ins.instances[0].key_name)

#First load config from the file

access_key="c74c3cb09b9a491095d58e9fd9f60c6b"
secret_key="ad1b3bd033104d7da905dd97725255e2"
instance_type="m1.large"
instances_config=[
        {"size":120,"type":"db"},
        {"size":120,"type":"db"},
    ]
region="melbourne-qh2"
sec_group=["ssh", "default"]
key_pair="proj"
image_name="ami-e2d5e55e"
volumn_type="melbourne"
output_header="[all:vars]\nansible_user=ubuntu\nansible_ssh_private_key_file=/Users/wtg/.ssh/id_rsa.pub"

#connect to ec2 server
conn = boto.connect_ec2(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        is_secure=True,
        region=RegionInfo(name=region, endpoint="nova.rc.nectar.org.au"),
        port=8773,
        path='/services/Cloud',
        validate_certs=False)

#write the host file
f=open("hosts","w+")
f.write(output_header+"\n\n")

#vol maps the VM types to lists of volumns
vols=dict()
#types maps the VM types to lists of IPs
types=dict()

for sz in instances_config:
    vol=create(sz["size"])
    if sz["type"] not in vols:
        vols[sz["type"]]=[vol]
    else:
        vols[sz["type"]].append(vol)

print ("Create Done, waiting for the instances...")
time.sleep(65)
print ("Getting instance info...")
#Re-fetch the instances' info. Now they should all finish spawning and the IPs should be vaild. 
all_inst=conn.get_all_reservations()
print_instances(all_inst)
count=0

#Bind the volumns with the VMs
for ty in vols:
    types[ty]=[]
    for vol in vols[ty]:
        print ("Attach volume of",ty)
        if conn.attach_volume(vol.id, all_inst[count].instances[0].id, "/dev/vdc"):
            print("Volume attache done!")
        else:
            print("Volume attache Failed!")
        types[ty].append(all_inst[count].instances[0].private_ip_address)
        count+=1

#Output IPs and VM types
for ty in types:
    f.write("[%s]\n" % ty)
    for ip in types[ty]:
        f.write(ip+"\n")
    f.write("\n")
f.close()


