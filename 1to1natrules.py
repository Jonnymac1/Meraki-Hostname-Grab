import requests
import json

url = "https://api.meraki.com/api/v0/organizations/570699/networks/L_686235993220591837/oneToOneNatRules"

payload = {}
headers = {
     'X-Cisco-Meraki-API-Key': '9c5a0265a76990f50ec54ec98fd0aa6e6ccbe1a4'
 }

response = requests.request("GET", url, headers=headers, data=payload)

allRules = json.loads(response.text)

for publicIp, value in allRules.items():
    print(publicIp, value)
    
#for deviceip in allRules:
    #print(allRules)
    #print("Model: {} \t Serial: {}".format(device["model"], device["serial"]))