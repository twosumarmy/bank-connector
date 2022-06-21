from enum import unique, Enum
from requests import Response

from bank_connector.authorization import AuthorizationCodeGrant
from bank_connector.client import BankClientBase


@unique
class Mode(Enum):
    Simulation = "https://api-sandbox.commerzbank.com"


class CommerzBankClient(BankClientBase, AuthorizationCodeGrant):

    def __init__(self):
        super().__init__(Mode.Simulation.value)

    def get_authorization_url(self, client_id: str, redirect_uri: str) -> str:
        path = "/auth/realms/sandbox/protocol/openid-connect/auth"
        return AuthorizationCodeGrant.format_authorization_url(self.base_url, path, client_id, redirect_uri)

    def get_access_token(self, client_id: str, client_secret: str, code: str, redirect_uri: str) -> Response:
        path = "/auth/realms/sandbox/protocol/openid-connect/token"
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(path=path, body=params, _headers=headers)
