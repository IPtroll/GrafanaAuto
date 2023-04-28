from grafana_client.elements.base import Base


class LibraryElement(Base):
    def __init__(self, client):
        super(LibraryElement, self).__init__(client)
        self.client = client

    def list_library_elements(self):
        """
        :return:
        """
        get_library_elements_path = "/library-elements"
        r = self.client.GET(get_library_elements_path)
        return r

    def get_library_element(self, library_element_uid):
        """
        :param library_element_uid:
        :return:
        """
        get_library_element_path = "/library-elements/%s" % library_element_uid
        r = self.client.GET(get_library_element_path)
        return r

    def get_library_element_by_name(self, library_element_name):
        """
        :param library_element_name:
        :return:
        """
        get_library_element_path = "/library-elements/name/%s" % library_element_name
        r = self.client.GET(get_library_element_path)
        return r

    def create_library_element(self, library_element):
        """
        :param library_element:
        :return:
        """
        create_library_element_path = "/library-elements"
        r = self.client.POST(create_library_element_path, json=library_element)
        return r

    def update_library_element(self, library_element):
        """
        :param library_element:
        :return:
        """
        update_library_element_path = "/library-elements/%s" % library_element["uid"]
        r = self.client.PATCH(update_library_element_path, json=library_element)
        return r


class Dashboard(Base):
    def __init__(self, client):
        super(Dashboard, self).__init__(client)
        self.client = client

    def get_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        get_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.client.GET(get_dashboard_path)
        return r

    def get_dashboard_by_name(self, dashboard_name):
        """

        :param dashboard_name:
        :return:
        """
        get_dashboard_path = "/dashboards/db/%s" % dashboard_name
        r = self.client.GET(get_dashboard_path)
        return r

    def update_dashboard(self, dashboard):
        """

        :param dashboard:
        :return:
        """

        # When the "folderId" is not available within the dashboard payload,
        # populate it from the nested "meta" object, if given.
        if "folderId" not in dashboard:
            if "meta" in dashboard and "folderId" in dashboard["meta"]:
                dashboard = dashboard.copy()
                dashboard["folderId"] = dashboard["meta"]["folderId"]

        put_dashboard_path = "/dashboards/db"
        r = self.client.POST(put_dashboard_path, json=dashboard)
        return r

    def delete_dashboard(self, dashboard_uid):
        """

        :param dashboard_uid:
        :return:
        """
        delete_dashboard_path = "/dashboards/uid/%s" % dashboard_uid
        r = self.client.DELETE(delete_dashboard_path)
        return r

    def get_home_dashboard(self):
        """

        :return:
        """
        get_home_dashboard_path = "/dashboards/home"
        r = self.client.GET(get_home_dashboard_path)
        return r

    def get_dashboards_tags(self):
        """

        :return:
        """
        get_dashboards_tags_path = "/dashboards/tags"
        r = self.client.GET(get_dashboards_tags_path)
        return r

    def get_dashboard_permissions(self, dashboard_id):
        """

        :param dashboard_id:
        :return:
        """
        get_dashboard_permissions_path = "/dashboards/id/%s/permissions" % dashboard_id
        r = self.client.GET(get_dashboard_permissions_path)
        return r

    def update_dashboard_permissions(self, dashboard_id, items):
        """

        :param dashboard_id:
        :param items:
        :return:
        """
        update_dashboard_permissions_path = (
            "/dashboards/id/%s/permissions" % dashboard_id
        )
        r = self.client.POST(update_dashboard_permissions_path, json=items)
        return r
