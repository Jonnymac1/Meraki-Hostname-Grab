import json
import requests
import codecs
import configparser
import os

requests.packages.urllib3.disable_warnings()

base_url_v1 = 'https://api.meraki.com/api/v1'

# Read configuration
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

apikey = config.get('settings', 'merakiapikey')
orgid = config.get('settings', 'merakiorgid')
filename = config.get('settings', 'export')

headers = {
	'x-cisco-meraki-api-key': format(str(apikey)),
	'Content-Type': 'application/json'
}

def __returnhandler(statuscode, returntext):
	if str(statuscode) == '200':
		return returntext
	else:
		print('HTTP Status Code: {0}\n'.format(statuscode))
def getorgdevices():
	results = []
	geturl = '{0}/organizations/{1}/devices?model=MX'.format(str(base_url_v1), str(orgid))
	dashboard = requests.get(geturl, headers=headers,verify=False)
	if dashboard.status_code == 200:
		raw = dashboard.json()
		for i in raw:  
			results.append(i)
		while 'next' in dashboard.links :
			dashboard = requests.get(dashboard.links['next']['url'],headers=headers,verify=False)
			raw = dashboard.json()
			for i in raw:  
				results.append(i)
	return (results)  
def getManagementInterface(serialnum):
	geturl = '{0}/devices/{1}/managementInterface'.format(str(base_url_v1), str(serialnum))
	dashboard = requests.get(geturl, headers=headers,verify=False)
	result = __returnhandler(dashboard.status_code, dashboard.text)
	return result
	
devices = getorgdevices()
f = codecs.open(filename, "a","utf-8")
f.write("DeviceName,activeDdnsHostname,ddnsHostnameWan1,ddnsHostnameWan2\n")
f.close()

for device in devices:
	ManagementInterface = json.loads(getManagementInterface(device['serial']))
	ActiveDDNSHostname = ManagementInterface['ddnsHostnames']['activeDdnsHostname']
	DDNSHostnameWan1 = ManagementInterface['ddnsHostnames']['ddnsHostnameWan1']
	DDNSHostnameWan2 = ManagementInterface['ddnsHostnames']['ddnsHostnameWan2']
	f = codecs.open(filename, "a","utf-8")
	message = "{},{},{},{}\n".format(device['name'],ActiveDDNSHostname,DDNSHostnameWan1,DDNSHostnameWan2)
	f.write(message)
	f.close()
