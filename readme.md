github-repo for grafana-client (grafana api for python)   https://github.com/panodata/grafana-client

installation of this library is requiered to connect to grafana_api (it can be installed anywhere if the grafana enviroment is availible through the internet, so not localhost)

upload_dashboard.py:

when this code runs it connects to grafana with credentials specified in config.yaml (admin cred. needed)
Then modifies the template dashboards based on machineID. In my example the dashboard templates are created once using grafana web gui and it takes advantage of grafana variables. A variable called machinID is created and then used in all influxdb queries (In my example there is one influxdb server and the unique identifier of the different data (temperature and humidity) is the machineID(which in my case are city names, such as budapest and berlin etc.). Then when creating a new dashboard for a new machineID a new folder is created for every machineID and dashboards are created from templates, and in the template files only the value of the machineID variable needs to be changed. (And one folder ID as well to make sure the menu bar works properly, and only lists dashboards that are in the same folder).

Within the same organization arbitrary number of new dashboards can be created. If you want to create dashboards in a different organization, just specify another orgID is the config.yaml file.  A little help for finding every organization and organization ID in the grafan enviroment is the grafana_org.py. It connects to the same grafana url specified in config.yaml and lists all the organizations with id-s.

