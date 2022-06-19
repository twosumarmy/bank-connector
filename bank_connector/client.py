import json
import logging
from requests import Response
from typing import Optional, Any, Callable, Dict

from bank_connector.session import get_requests_session


class BankClientBase:
    """Bank Client with low-level HTTP operations"""

    def __init__(
            self, base_url, request_timeout: Optional[int] = None, verbose=False
    ) -> None:
        self.log = logging.getLogger("BankClientBase")
        if verbose:
            self.log.setLevel(logging.DEBUG)
        self.base_url = base_url
        self.session = get_requests_session(timeout=request_timeout)
        self.access_token: Optional[str] = None

    def set_access_token(self, access_token: str) -> None:
        self.access_token = access_token

    def _process_request(
            self, func: Callable, path: str, body: Any, params: Any = None, _headers: Optional[Dict] = None
    ) -> Response:
        url = self.base_url + path
        headers = _headers.copy() if _headers else {}
        if self.access_token:
            headers['Authorization'] = f"Bearer {self.access_token}"
        response: Response = func(url, headers=headers, params=params, data=body)

        self.log.debug(f"status_code: {response.status_code}")
        if response.headers.get("content-type") == "application/json":
            self.log.debug(json.dumps(response.json(), sort_keys=True, indent=4))
        else:
            self.log.debug(response.text)

        return response

    def get(self, path: str = "", params: Any = None, _headers: Optional[Dict] = None) -> Response:
        """HTTP GET"""
        return self._process_request(self.session.get, path, None, params=params, _headers=_headers)

    def post(self, path: str = "", body: Any = None, params: Any = None, _headers: Optional[Dict] = None) -> Response:
        """HTTP POST"""
        return self._process_request(self.session.post, path, body, params=params, _headers=_headers)
