import json
import sys

from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError
import os
from library_element import LibraryElement


def import_plot_by_name(api, name, uid):
    library_element = LibraryElement(api.client).get_library_element_by_name(name)[
        "result"
    ][0]
    obj = {
        "folderUid": "",
        "uid": uid,
        "name": name,
        "type": library_element["type"],
        "kind": library_element["kind"],
        "description": library_element["description"],
        "model": {
            "datasource": library_element["model"]["datasource"],
            "description": library_element["model"]["description"],
            "libraryPanel": {
                "description": library_element["description"],
                "name": name,
                "uid": uid,
                "type": library_element["type"],
            },
            "options": library_element["model"]["options"],
            "targets": library_element["model"]["targets"],
            "title": name,
            "transformations": library_element["model"]["transformations"]
            if "transformations" in library_element["model"]
            else [],
            "transparent": library_element["model"]["transparent"],
            "type": library_element["type"],
        },
    }
    open("library/plots/%s.json" % uid, "w").write(json.dumps(obj, indent=2))


def update_library_element(api, uid):
    obj = json.loads(open(f"library/plots/{uid}.json").read())
    # check if exists
    try:
        exist = LibraryElement(api.client).get_library_element(obj["uid"])
        obj["version"] = exist["result"]["version"]
        LibraryElement(api.client).update_library_element(obj)
        return True
    except GrafanaClientError as e:
        print(e)
        return False


def create_library_element(api, uid):
    # print(api.organizations.switch_organization(org_id))
    obj = json.loads(open(f"library/plots/{uid}.json").read())
    try:
        exists = LibraryElement(api.client).get_library_element_by_name(obj["name"])[
            "result"
        ][0]
        print(f"element with name already exists for {uid}, {obj['name']}")

        return False
        # print(LibraryElement(api).update_library_element({"uid": exists["uid"], "name": exists["name"]+"-old"}))
        # print("renamed")
    except GrafanaClientError as e:
        pass

    try:
        LibraryElement(api.client).create_library_element(obj)
        return True
    except GrafanaClientError as e:
        print(e)
        return False


def create_datasource(api, uid):
    obj = json.loads(open(f"library/data_sources/{uid}.json").read())
    try:
        api.datasource.create_datasource(obj)
        return True
    except GrafanaClientError as e:
        print(e)
        return False
