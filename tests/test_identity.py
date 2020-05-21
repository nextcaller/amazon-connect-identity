from copy import deepcopy

import pytest
import requests
import responses

import identity

mock_user_base = {
    "address": {
        "city": "New York",
        "first_name": "Jane",
        "last_name": "Smith",
        "line1": "123 Fake St.",
        "line2": None,
        "state": "NY",
        "zip": "10001",
    },
    "close_link": "/address_transactions/foo-bar-1234/close",  # noqa
    "confirmation_link": "/address_transactions/foo-bar-1234/0/confirm",  # noqa
    "confirmed": False,
    "id": "foo-bar-1234",
    "phone": "+12125551212",
}
user_with_l2 = deepcopy(mock_user_base)
user_with_l2["address"].update({"line2": "Apt A"})
user_with_no_result = deepcopy(mock_user_base)
user_with_no_result.update({"address": None, "confirmation_link": None})


@responses.activate
@pytest.mark.parametrize(
    "user_data,lookup_result,expected",
    [
        (
            {"phone": "12125551212"},
            mock_user_base,
            {
                "FirstName": "Jane",
                "LastName": "Smith",
                "AddressL1": "123 Fake St.",
                "AddressL2": None,
                "City": "New York",
                "State": "NY",
                "Zip": "10001",
                "CloseUrl": "https://example.com/address_transactions/foo-bar-1234/close",  # noqa
                "ConfirmationUrl": "https://example.com/address_transactions/foo-bar-1234/0/confirm",  # noqa
            },
        ),
        (
            {"phone": "12125551212"},
            user_with_l2,
            {
                "FirstName": "Jane",
                "LastName": "Smith",
                "AddressL1": "123 Fake St.",
                "AddressL2": "Apt A",
                "City": "New York",
                "State": "NY",
                "Zip": "10001",
                "CloseUrl": "https://example.com/address_transactions/foo-bar-1234/close",  # noqa
                "ConfirmationUrl": "https://example.com/address_transactions/foo-bar-1234/0/confirm",  # noqa
            },
        ),
        (
            {"phone": "12125551212"},
            user_with_no_result,
            {
                "FirstName": None,
                "LastName": None,
                "AddressL1": None,
                "AddressL2": None,
                "City": None,
                "State": None,
                "Zip": None,
                "CloseUrl": "https://example.com/address_transactions/foo-bar-1234/close",  # noqa
                "ConfirmationUrl": None,
            },
        ),
    ],
)
def test_get_address(user_data, lookup_result, expected):
    responses.add(
        responses.POST,
        "https://example.com/address_transactions",
        json=lookup_result,
        status=200,
    )

    address_lookup = identity.AddressTransaction(
        host="example.com", username="foo", password="bar"
    )

    r = identity.get_address(address_lookup, user_data)

    assert r == expected


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

    r = identity.confirm_address(address_lookup, url)

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

    r = identity.close_address_tx(address_lookup, url)

    assert r == expected
