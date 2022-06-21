from abc import ABC, abstractmethod
from urllib.parse import urlencode, urljoin
from requests import Response


class AuthorizationCodeGrant(ABC):
    """The authorisation code grant flow first gets a code and then exchanges it for an access token."""

    @abstractmethod
    def get_authorization_url(self, client_id: str, redirect_uri: str) -> str:
        pass

    @abstractmethod
    def get_access_token(self, client_id: str, client_secret: str, code: str, redirect_uri: str) -> Response:
        pass

    @staticmethod
    def format_authorization_url(base_url: str, path: str, client_id: str, redirect_uri: str) -> str:
        query = "?" + urlencode(dict(response_type="code", client_id=client_id, redirect_uri=redirect_uri))
        return urljoin(base_url, path + query)
