import prometeo

class SandboxClient(prometeo.banking.BankingAPIClient):
    ENVIRONMENTS = {
        'sandbox': 'https://banking.sandbox.prometeoapi.com'
    }

class ClientWrapper(prometeo.Client):

    def __init__(self, api_key, environment):
        super().__init__(api_key, environment)
        self._api_key = api_key
        self._environment = environment


    @property
    def banking(self):
        self._banking = prometeo.banking.BankingAPIClient(self._api_key, self._environment)
        return self._banking


class PrometeoClient(ClientWrapper):

    def __init__(self, api_key, environment):
        super().__init__(api_key, environment)
        self._client = ClientWrapper(api_key, environment=environment)

    def login(self, provider, username, password, **kwargs):
        session = self._client.banking.login(provider, username, password, **kwargs)
        return session.get_session_key()

    def logout(self):
        self._client.banking.logout()





