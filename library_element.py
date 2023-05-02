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
