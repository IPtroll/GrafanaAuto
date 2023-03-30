 # Generate Grafana Org,User,Page,Flux query,

#getAdmin 
grafana_admin = "admin"
admin_password = "bmeKTH"

# Read _MachineConfig_


# Generate _ORG_ from _MachineConfig_


# Generate influx _BUCKET_ from _MachineConfig_


# Generate _USER_ from _MachineConfig_
'''
with open("MID_X0_M221213.json") as json_data_file:
    machineInfo = json.load(json_data_file)
'''
name = 'AlfonsÅberg'
username = 'AlfonsÅberg'
user_email = 'alfons@aberg.se'
password = ''

# Add _USER_ to _ORG_


# Deploy CustomerJourneyStep1 page
# Deploy CustomerJourneyStep2 page
# Deploy CustomerJourneyStep3 page
# Deploy CustomerJourneyStep4 page

#________
# pip install fsspec
# pip install s3fs

import pandas as pd 
import json 
import sys
import yaml
#from grafana_api.grafana_face import GrafanaFace
from grafana_client import GrafanaApi
import secrets
import os 


from influxdb_client import InfluxDBClient, BucketRetentionRules

# Generate _ORG_ from _MachineConfig_

with open('./config/config.yaml','r') as conf:
    global config
    config=yaml.load(conf)

#use grafana admin api 
grafana_api = GrafanaApi.from_url(
    url=config["grafana_url"],
    credential=(grafana_admin, admin_password)
)


#data = pd.read_csv("s3://ipercept-data/META/MID_X0_M221213/MID_X0_M221213.json", header=None).squeeze("columns")

with open("MID_X0_M221213.json") as json_data_file:
    machineInfo = json.load(json_data_file)

orgname = machineInfo['company']

#Add new organization
print(grafana_api.organization.create_organization(organization={"name": orgname}))
print(grafana_api.organizations.list_organization())

OrgNameIDList = grafana_api.organizations.list_organization()

for i in range(len(OrgNameIDList)):
    if OrgNameIDList[i]['name'] == orgname:
        orgID = OrgNameIDList[i]['id']

print(orgID)


# Generate _USER_ from _MachineConfig_
'''
uname = machineInfo['uname']
user = machineInfo['user']
user_email = machineInfo['user_email']
'''
password = secrets.token_urlsafe(12)

command = 'echo ' + password + ' >> pass.txt'
os.system(command)

# Create user
# Add _USER_ to _ORG_
user = grafana_api.admin.create_user({
    "name": name, 
    "login": username, 
    "email": user_email, 
    "password": password, 
    "OrgId": orgID,
})


#         SLACK
'''
orden = 'New autogenerated Grafana user!  \n  username: ' + name + '  '  + 'email: ' +  user_email + '  temporary password: ' + password + '  company: ' + orgname
theCommand = "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"" + orden + "\"}' https://hooks.slack.com/services/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 "
os.system(theCommand)
'''


"""
Define Influx credentials
"""
url = "http://16.170.107.243:8086/" 
token = "VI30zdLHoiSfIHoZtDZH_7JR-mq2RyjGT4kuf6XfNNeE_vDSQ2ukR2CcVl158oGfrJKza5YdKbvys3qrE8YhuA=="
InfluxOrg = "IPercept"

with InfluxDBClient(url=url, token=token) as client:
    buckets_api = client.buckets_api()
    """
    Create Bucket with OrgID
    """
    print(f"------- Create -------\n")
    #retention_rules = BucketRetentionRules(type="expire", every_seconds=3600)
    retention_rules=None
    created_bucket = buckets_api.create_bucket(bucket_name=orgID,   #  Create Bucket with OrgID
                                               retention_rules=retention_rules,
                                               org=InfluxOrg)
    print(created_bucket)


####################################
# Deploy CustomerJourneyStep1 page #
####################################

l=0
while (l<len(config["machineID_list"])):
    machineID=config["machineID_list"][l]
#### Try to create folder with same title and uid  as machine ID
    try:
        grafana_api.folder.create_folder(title=machineID,uid=machineID)
        print("[INFO] '"+machineID+"' folder created successfully. \n")
    except Exception as e: 
        
        print("[WARNING] Folder cannot be created. "+str(e)+"\n")

    # get folderID of the folder just created
    folderID=grafana_api.folder.get_folder(uid=machineID)["id"]
    print("[INFO] Folder found with uid: "+machineID+". The FolderID is: "+str(folderID)+"\n")


   

    #### Go through template_file_list and create dashboards in a folder

    i=0
    while (i<page_num):

        with open("./templates/"+template_file_list[i], 'r') as fcc_file:
            fcc_data = json.load(fcc_file)
            ### Find grafana variable in json and insert machineid as value. This is mainly for indluxdb queries
            fcc_data["templating"]["list"][0]["query"]=machineID
            ### find folder id in "menu" to only display dashboards in a specific folder
            i_panel=0
            print(len(fcc_data["panels"]))
            while i_panel in range(len(fcc_data["panels"])):
                if (  "title" in fcc_data["panels"][i_panel] and (fcc_data["panels"][i_panel]["title"]=="Menu")):
                    fcc_data["panels"][i_panel]["options"]["folderId"]=folderID ##Find menu panel by title "Menu"
                    #print("[DEBUG]Title")
                elif("datasource" in fcc_data["panels"][i_panel]):
                    fcc_data["panels"][i_panel]["datasource"]["uid"]=datasource_uid
                i_panel+=1
                
                    


            fcc_data["folderId"]=folderID
            fcc_data["uid"]=None
            fcc_data["id"]=None
            
        
            
            
            edit_data=json.dumps(fcc_data,indent=4)
            #print (edit_data)
            dashboard_payload={
                "dashboard": fcc_data ,
                "overwrite": False , # if you want to overwrite existing dashboards set this variable true
                "folderId": folderID,
                "message": "Updated by grafana API"
            }
            #print(dashboard_payload)
            try:
                response=grafana_api.dashboard.update_dashboard(dashboard_payload)
                print("[INFO] Grafana Dashboard Update Response: "+str(response)+"\n")
            except Exception as e: print("[WARNING] Dashboard was not created. "+str(e)+"\n")
    
        i+=1
    l+=1



