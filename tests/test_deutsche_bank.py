from unittest.mock import patch

from bank_connector.client import BankClientBase
from bank_connector.banks.deutsche_bank import DeutscheBankClient


class TestDeutscheBankClient:

    def test_get_cash_accounts(self):
        client = DeutscheBankClient()
        with patch.object(BankClientBase, 'get', return_value={}) as mock_get:
            client.get_cash_accounts()
            mock_get.assert_called_once_with(path="/gw/dbapi/banking/cashAccounts/v2")

    def test_get_transactions(self):
        client = DeutscheBankClient()
        with patch.object(BankClientBase, 'get', return_value={}) as mock_get:
            client.get_transactions("iban123")
            mock_get.assert_called_once_with(
                path="/gw/dbapi/banking/transactions/v2",
                params={
                    "iban": "iban123"
                }
            )
