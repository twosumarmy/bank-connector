from requests import adapters, models, Session
from requests.structures import CaseInsensitiveDict
from typing import Any, Optional

from bank_connector import __version__


class BankClientAdapter(adapters.HTTPAdapter):
    def __init__(self, *args: Any, timeout: Optional[int] = None, **kwargs: Any) -> None:
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, *args: Any, **kwargs: Any) -> models.Response:
        if not kwargs.get("timeout"):
            kwargs["timeout"] = self.timeout
        return super().send(*args, **kwargs)


def get_requests_session(*, timeout: Optional[int] = None) -> Session:
    adapter = BankClientAdapter(timeout=timeout)
    session = Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.verify = True
    session.headers = CaseInsensitiveDict(
        {
            "user-agent": f"bank-connector/{__version__}",
        }
    )
    return session
