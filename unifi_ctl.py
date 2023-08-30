from unificontrol import UnifiClient
import pprint as pp
import socket
import ipaddress 
import pandas as pd

site = "r3tagyo7"
#site = "default"
controller = "172.20.197.148"
#controller = "3.208.83.14"
client = UnifiClient(host=controller,
    username="rsupport", password="elrbsestNF!25", site=site)

lista = client.list_devices()

def sort_by_ip(lista):
#	sorted_list = sorted(lista, key=lambda d: d['ip'])
	return sorted(lista, 
				key = lambda machine_role: (machine_role["ip"],
											socket.inet_aton(machine_role["ip"])))


tags =  client.list_tags()
def get_id(mac):
	for device in lista:
		if mac == device['mac']:
			return device['_id']

def search_tag(mac):
	for tag in tags:
		if mac in tag.get('member_table', 'none'):
			return tag['name']
	else:
		return "none"

def get_uplink(uplink):
	if uplink != "none":
		for i in lista:
			if uplink.get('uplink_mac','none') == i['mac']:
				uplink_name = i.get('name','none')
				uplink_remote_port = uplink.get('uplink_remote_port','wireless')
		#uplink_name = [ i['name'] for i in lista if i['mac']==uplink] 
		return uplink_name,uplink_remote_port
	else:
		return "none","none"

def sort_by_ip(ips):
	return sorted(lista, key=lambda x: int(ipaddress.ip_address(x['ip'])))

def export_excel(devices):
	df = pd.DataFrame(data=devices)
	#convert into excel
	df.to_excel("devices.xlsx", index=False)

def parse_model_name(model):
	models = {
				"U7LR": "UAP AC LR", 
				"U7PG2" : "UAP-AC-Pro",
				"U7HD" : "UAP AC HD",
				"UALR6v2" : "U6 LR",
				"BZ2LR" : "UAP LR",
				"BZ2" : "UAP"
				}
	return models[model]


def show_devices(lista):
	device_list = []
	for ap_device in sort_by_ip(lista):
		if ap_device['type'] == 'uap': 
			# dev_mac = ap_device['mac']
			# dev_name = ap_device.get('name','none')
			# dev_ip = ap_device['ip']
			uplink = ap_device.get('uplink','none')
			#print(uplink)
			dev_uplink, port = get_uplink(uplink)
			#print(f'{dev_mac} {dev_ip} {uplink}')
			#print(ap_device['type'],ap_device['ip'], ap_device['name'], search_tag(ap_device['mac']),dev_uplink,port)
			device_list.append({
				"name" : ap_device.get('name','none'),
				"ip" : ap_device['ip'],
				"mac" : ap_device.get('mac','none'),
				"model" : parse_model_name(ap_device['model']),
				"uplink" : dev_uplink,
				"uplink_port" : port,
				"loc" : search_tag(ap_device['mac'])
			})
	return device_list
# for aps in lista:
# 	if aps['mac'] == mac:
# 		ap_id = aps["_id"]



#print(ap_id)

#name = "BUEMB"+str
def change_ap_name():
	index = 11
	for ap_device in sort_by_ip(lista):
		# if ap_device['state'] == 1 and ap_device['type'] == 'uap':
		if ap_device['type'] == 'uap':
			numeric_name = ap_device['name'].split("BUEMB")
			name = "BUEMBAP"+numeric_name[1]
			index +=1
			try:
				# print("BUEMBAP"+numeric_name[1])	
				client.rename_ap(ap_device["_id"], name)
				print("cambiando ap "+ap_device['name']+" por el nombre "+name)
			except:
				print("error al cambiar nombre ")
#mac = "fc:ec:da:31:e0:ef"
#id_device = get_id(mac)
show_devices(lista)
change_ap_name()