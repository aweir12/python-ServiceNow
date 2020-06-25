class ServiceNowInstance():
    """
    Class to capture/store information on how to connect
    to an instance of ServiceNow via RESTful api

    Parameters
    ----------
    subdomain: str or None
        Subdomain of the ServiceNow instance
    api_user: str
        ServiceNow username with API access
    api_password: str
        Password for api_user
    """

    def __init__(self, subdomain, api_user, api_password):
        self.subdomain = subdomain
        self.api_user = api_user
        self.api_password = api_password

    def _table_url_construct(self, table, offset, limit, reference_link):
        url = ("https://{}.service-now.com/api/now/table/{}"
               "?sysparm_exclude_reference_link={}&sysparm_offset={}"
               "&sysparm_limit={}")
        return url.format(self.subdomain, table, str(not reference_link),
                          offset, limit)

    def _table_count_construct(self, table):
        url = ("https://{}.service-now.com/api/now/v1/stats/{}"
               "?sysparm_count=true")
        return url.format(self.subdomain, table)

    def _retrieve_data(self, query_string):
        import requests
        with requests.Session() as session:
            session.headers = {}
            session.auth = (self.api_user, self.api_password)
            result = session.get(query_string)
        return result
