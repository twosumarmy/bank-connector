from bank_connector.authorization import AuthorizationCodeGrant


class TestAuthorizationCodeGrant:
    def test_format_authorization_url(self):
        expected = "https://simulator-api.db.com/gw/oidc/authorize?response_type=code&client_id=foo&redirect_uri=bar"
        assert AuthorizationCodeGrant.format_authorization_url(
            "https://simulator-api.db.com", "/gw/oidc/authorize", "foo", "bar"
        ) == expected
