import base64
from enum import Enum, unique
from requests import Response
from urllib.parse import urlencode, urljoin

from bank_connector.client import BankClientBase


@unique
class Mode(Enum):
    Simulation = "https://simulator-api.db.com"


class DeutscheBankClient(BankClientBase):
    """Deutsche Bank Client with high-level operations"""

    def __init__(self):
        base_url = Mode.Simulation.value
        super().__init__(base_url)

    def get_authorize_url(self, client_id: str, redirect_uri: str):
        """Get the url for login and grant access pages"""
        return self._format_authorize_url(client_id, redirect_uri)

    def _format_authorize_url(self, client_id: str, redirect_uri: str) -> str:
        path = "/gw/oidc/authorize"
        query = "?" + urlencode(dict(response_type="code", client_id=client_id, redirect_uri=redirect_uri))
        return urljoin(self.base_url, path + query)

    def get_access_token(self, client_id: str, client_secret: str, code: str, redirect_uri: str) -> Response:
        """Request access token with given code"""
        path = "/gw/oidc/token"
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        encoded_string = base64.b64encode(f"{client_id}:{client_secret}".encode("ascii")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {encoded_string}"
        }
        response = self.post(path=path, params=params, _headers=headers)
        return response

    def get_cash_accounts(self) -> Response:
        """Get cash account information"""
        path = "/gw/dbapi/banking/cashAccounts/v2"
        response = self.get(path=path)
        return response

    def get_transactions(self, iban: str) -> Response:
        """Get transactions for cash accounts"""
        path = "/gw/dbapi/banking/transactions/v2"
        params = {
            "iban": iban
        }
        response = self.get(path=path, params=params)
        return response
