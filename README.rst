bank-connector |BuildStatus|_
==============

.. |BuildStatus| image:: https://github.com/twosumarmy/bank-connector/actions/workflows/build.yaml/badge.svg
.. _BuildStatus: https://github.com/twosumarmy/bank-connector/actions

This project contains clients for multiple bank APIs.

Following bank APIs are supported:

* `Deutsche Bank API <https://developer.db.com/>`_

Usage
=====

Get account balance and transactions for cash accounts::

    from bank_connector.banks.deutsche_bank import DeutscheBankClient

    client = DeutscheBankClient()
    client.set_access_token("token")

    client.get_cash_accounts()
    client.get_transactions("iban123")

