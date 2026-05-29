from __future__ import annotations


def test_bitfinex_transport_modules_import_without_activation() -> None:
    import core.io.bitfinex.exchange_client as exchange_client
    import core.io.bitfinex.read_helpers as read_helpers
    import core.io.bitfinex.rest_auth as rest_auth
    import core.io.bitfinex.rest_public as rest_public
    import core.io.bitfinex.ws_auth as ws_auth
    import core.io.bitfinex.ws_public as ws_public
    import core.io.bitfinex.ws_reconnect as ws_reconnect

    assert exchange_client.__name__ == "core.io.bitfinex.exchange_client"
    assert read_helpers.__name__ == "core.io.bitfinex.read_helpers"
    assert rest_auth.__name__ == "core.io.bitfinex.rest_auth"
    assert rest_public.__name__ == "core.io.bitfinex.rest_public"
    assert ws_auth.__name__ == "core.io.bitfinex.ws_auth"
    assert ws_public.__name__ == "core.io.bitfinex.ws_public"
    assert ws_reconnect.__name__ == "core.io.bitfinex.ws_reconnect"
