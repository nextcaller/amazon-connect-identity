from copy import deepcopy

import pytest
import requests
import responses

import identity


@responses.activate
@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://example.com/address_transactions/foo-bar-1234/0/confirm",
            {"message": "Success!"},
        ),
        (
            "https://example.com/address_transactions/foo-bar-1234/0",
            {
                "message": (
                    "The requested URL was not found on the server. "
                    "If you entered the URL manually please check your "
                    "spelling and try again."
                )
            },
        ),
    ],
)
def test_confirm_address(url, expected):
    responses.add(
        responses.POST, url, json=expected, status=200,
    )

    address_lookup = identity.AddressTransaction(
        host="example.com", username="foo", password="bar"
    )

    r = identity.finalize_tx(address_lookup, url)

    assert r == expected


@responses.activate
@pytest.mark.parametrize(
    "url,expected",
    [
        (
            "https://example.com/address_transactions/foo-bar-1234/close",
            {"message": "Success!"},
        ),
        (
            "https://example.com/address_transactions/foo-bar-1234/0",
            {
                "message": (
                    "The requested URL was not found on the server. "
                    "If you entered the URL manually please check your "
                    "spelling and try again."
                )
            },
        ),
    ],
)
def test_close_address_tx(url, expected):
    responses.add(
        responses.POST, url, json=expected, status=200,
    )

    address_lookup = identity.AddressTransaction(
        host="example.com", username="foo", password="bar"
    )

    r = identity.finalize_tx(address_lookup, url)

    assert r == expected
