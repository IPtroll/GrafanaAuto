from curses import KEY_MARK, init_pair
import json
import sys
import yaml
#from grafana_api.grafana_face import GrafanaFace
from grafana_client import GrafanaApi
import csv





#open config file in config folder
with open('./config/config.yaml','r') as conf:
    global config
    config=yaml.load(conf)

#use grafana admin api 

grafana_api = GrafanaApi.from_url(
    url=config["grafana_url"],
    credential=(config["grafana_admin"], config["admin_password"])
)




# switch organization to specified orgID
grafana_api.organizations.switch_organization(config["orgID"])

# list of the template files (the pages of the dashboard)
template_file_list=config['templateFileList']

#number of pages
page_num=len(template_file_list)

#machineID read from the config file
#machineID=config['machineID']

print("[INFO] Current Organization: "+str(grafana_api.organization.get_current_organization())+"\n")


#Get uid of datasource specified in config.yaml
global datasource_uid
datasource_uid=grafana_api.datasource.get_datasource_by_name(config["datasource_name"])["uid"]
print(datasource_uid)
#### Go through all the machineID-s provided in the config.yaml file
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

######### User creation ##########

with open ("./config/"+config["user_csv"],newline='\n') as user_file:
    reader = csv.reader(user_file)
    user_csv = list(reader)

for user in user_csv:
    # Create user
    user = grafana_api.admin.create_user({
        "name": user[0], 
        "email": user[1], 
        "login": user[2], 
        "password": user[3], 
        "OrgId": config["orgID"],
    })
    #print(user[1])
    #print("\n")
 



