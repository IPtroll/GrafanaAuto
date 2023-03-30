import json
import sys
import yaml
#from grafana_api.grafana_face import GrafanaFace
from grafana_client import GrafanaApi

# Use Grafana API token.
#grafana_api = GrafanaApi.from_url(
 #   url="http://localhost:3000/", credential="eyJrIjoiR05TRTNiblY5a2pTUzVUN1dyQjBYU1JBVnByTWdMeUYiLCJuIjoiR3JhZmFuYV9hcGkiLCJpZCI6Mn0=",
#)


grafana_api = GrafanaApi.from_url(
    url="https://localhost:3000/grafana/",
    credential=("admin", "Ud98%2Lm")
)







#grafana_api = GrafanaFace(auth='eyJrIjoiR05TRTNiblY5a2pTUzVUN1dyQjBYU1JBVnByTWdMeUYiLCJuIjoiR3JhZmFuYV9hcGkiLCJpZCI6Mn0=', host='localhost:3000') 

with open('config.yaml','r') as conf:
    global config
    config=yaml.load(conf)


template_file_list=config['templateFileList']
page_num=len(template_file_list)

machineID=config['machineID']
i=0




print("## All folders on grafana", file=sys.stderr)
folders = grafana_api.folder.get_all_folders()

folders_json=json.dumps(folders, indent=2)
print(folders_json)

folders_length=len(folders)
print(folders_length)


while (i<folders_length) :
    global folderID
    
    if (folders[i]["title"] == machineID):
        folderID=folders[i]["id"]
        print(folderID)
    i+=1


i=0
while (i<1):

    with open(template_file_list[0], 'r') as fcc_file:
        fcc_data = json.load(fcc_file)
        fcc_data["templating"]["list"][0]["query"]=machineID
        fcc_data["panels"][3]["options"]["folderId"]=folderID
       
        
        print("\n \n \n \n ")
        edit_data=json.dumps(fcc_data,indent=4)
        #print (edit_data)
        #grafana_api.dashboard.update_dashboard(dashboard={'dashboard': edit_data , 'folderId': 0, 'overwrite': True})
 

    with open('edited'+template_file_list[i],'w') as f_edit:
        f_edit.write(edit_data)
        
    i+=1


