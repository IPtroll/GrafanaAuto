#python3.9
import json
import sys
import yaml
#from grafana_api.grafana_face import GrafanaFace
from grafana_client import GrafanaApi


#open config file in config folder
with open('./config/config.yaml','r') as conf:
    global config
    config=yaml.load(conf)

grafana_api = GrafanaApi.from_url(
    url=config["grafana_url"],
    credential=(config["grafana_admin"], config["admin_password"])
)

print(grafana_api.datasource.list_datasources())