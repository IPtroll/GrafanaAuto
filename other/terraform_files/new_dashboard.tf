terraform {
  required_providers {
    grafana = {
      source = "grafana/grafana"
    }
  }
}




provider "grafana" {
  url  = yamldecode(file("Dashboard_Template/config.yaml"))["grafana_url"]  
  auth = yamldecode(file("Dashboard_Template/config.yaml"))["grafana_auth"]
}

resource "grafana_folder" "folders" {
  
  for_each = toset(yamldecode(file("Dashboard_Template/config.yaml"))["grafana_folder"])
  title = yamldecode(file("Dashboard_Template/config.yaml"))["grafana_folder"]
  

  resource "grafana_dashboard" "dashboards" {
    for_each= toset(yamldecode(file("Dashboard_Template/config.yaml"))["templateFileList"])
    config_json = file("Dashboard_Template/edited${each.key}")
    folder = grafana_folder.folders.id
  }
}


