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
