"""
Copyright 2016 Ashok Kanagarasu

These are sample functions for the Cisco Fog Director REST API.

Below code is to 
    1. List all the apps added to FD with publish status.
    
See: 

http://www.cisco.com/c/en/us/td/docs/routers/access/800/software/guides/iox/fog-director/reference-guide/1-0/fog_director_ref_guide.html

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import requests
import json
import base64

def get_token(ip,username,password):
    #print(ip)
    url = "https://%s/api/v1/appmgr/tokenservice" % ip
    print(url)

    r = requests.post(url,auth=(username,password),verify=False)
    token=''
    if  r.status_code == 202:
        print(r.json())
        token = r.json()['token']
        #print(token)
    else:
        print("ERROR")
        print "Status code is "+str(r.status_code)
        print r.text
    return(token)

def delete_token(ip, token):
    url = "https://%s/api/v1/appmgr/tokenservice/%s" % (ip, token)
	
    headers = {'x-token-id':token,'content-type': 'application/json'}
    
    r = requests.delete(url,headers=headers,verify=False)

    if  r.status_code == 200:
        print(r.json())
    else:
        print("ERROR")
        print "Status code is "+str(r.status_code)
        print r.text	
		
def get_apps(ip, token):
    url = "https://%s/api/v1/appmgr/localapps?limit=100" % ip
    headers = {'x-token-id':token,'content-type': 'application/json'}
    r=requests.get(url,headers=headers,verify=False)
    print(r.status_code)
    
    apps=json.loads((json.dumps(r.json())))

    print apps['data']
    
    for index in range(len(apps['data'])):
        appid=apps['data'][index]['localAppId']
        appname=apps['data'][index]['name']
        publish_state=apps['data'][index]['published']
        print "App with name '%s' , appid '%s'  and published status is '%s'" %(appname, appid, publish_state)
        print apps['data'][index]
                        
app_mgr_ip=raw_input("Enter app manager ip address: ")
username=raw_input("Enter the username of your FD: ")
password=raw_input("Enter the password of your FD: ")

#Login to Fog Director
print "Login to Fog Director"
token_id=get_token(app_mgr_ip,username,password)
print(token_id)

print "Get apps added to Fog Director" 
get_apps(app_mgr_ip, token_id)

print "Logging out of Fog Director"
delete_token(app_mgr_ip, token_id)