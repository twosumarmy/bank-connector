import base64
from enum import Enum, unique
from requests import Response

from bank_connector.authorization import AuthorizationCodeGrant
from bank_connector.client import BankClientBase


@unique
class Mode(Enum):
    Simulation = "https://simulator-api.db.com"


class DeutscheBankClient(BankClientBase, AuthorizationCodeGrant):
    """Deutsche Bank Client with high-level operations"""

    def __init__(self):
        super().__init__(Mode.Simulation.value)

    def get_authorization_url(self, client_id: str, redirect_uri: str) -> str:
        path = "/gw/oidc/authorize"
        return AuthorizationCodeGrant.format_authorization_url(self.base_url, path, client_id, redirect_uri)

    def get_access_token(self, client_id: str, client_secret: str, code: str, redirect_uri: str) -> Response:
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
        return self.post(path=path, params=params, _headers=headers)

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
