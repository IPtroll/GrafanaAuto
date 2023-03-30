import json
import sys
import yaml
#from grafana_api.grafana_face import GrafanaFace
from grafana_client import GrafanaApi

with open('./config/config.yaml','r') as conf:
    global config
    config=yaml.load(conf)

#use grafana admin api 

grafana_api = GrafanaApi.from_url(
    url=config["grafana_url"],
    credential=(config["grafana_admin"], config["admin_password"])
)



print("[grafana_org] List of grafana organizations: ")
print(grafana_api.organizations.list_organization())


#Add new organization
print(grafana_api.organization.create_organization(organization={"name": "testOrg"}))


print(grafana_api.organizations.list_organization())