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


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {
                "addresses": [
                    {
                        "city": "New York",
                        "zip": "10013",
                        "state": "NY",
                        "line1": "123 Fake St",
                        "line2": None,
                    },
                    {
                        "city": "Los Angeles",
                        "zip": "90010",
                        "state": "CA",
                        "line1": "123 Fake St",
                        "line2": None,
                    },
                ],
                "close_link": "/address_transactions/id-1234/close",
                "confirmation_link": "/address_transactions/id-1234/0/confirm",
                "confirmed": False,
                "first_name": "Jane",
                "id": "id-1234",
                "last_name": "Smith",
                "phone": "+12125551212",
                "retry_link": None,
                "zip": None,
            },
            {
                "city": "New York",
                "close_link": "/address_transactions/id-1234/close",
                "confirmation_link": "/address_transactions/id-1234/0/confirm",
                "confirmed": False,
                "first_name": "Jane",
                "id": "id-1234",
                "last_name": "Smith",
                "line1": "123 Fake St",
                "line2": None,
                "phone": "+12125551212",
                "retry_link": None,
                "state": "NY",
                "zip": "10013",
            },
        ),
        (
            {
                "addresses": None,
                "close_link": "/address_transactions/id-1234/close",
                "confirmation_link": None,
                "confirmed": False,
                "first_name": None,
                "id": "id-1234",
                "last_name": None,
                "phone": "+12125551212",
                "retry_link": None,
                "zip": None,
            },
            {
                "close_link": "/address_transactions/id-1234/close",
                "confirmation_link": None,
                "confirmed": False,
                "first_name": None,
                "id": "id-1234",
                "last_name": None,
                "phone": "+12125551212",
                "retry_link": None,
                "zip": None,
            },
        ),
    ],
)
def test_flatten_address_data(data, expected):
    output = identity.flatten_address_data(data)
    assert output == expected
