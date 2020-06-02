import os
import json

from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.logging import Logger

import identity

tracer = Tracer()
logger = Logger()

host = os.environ["API_ENDPOINT"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

address_lookup = identity.AddressTransaction(
    host=host, username=username, password=password
)


@tracer.capture_lambda_handler
def handler(event, context):
    contact_data = event["Details"].get("ContactData")
    parameters = event["Details"].get("Parameters", {})
    contact_id = contact_data["ContactId"]

    request_type = parameters.get("AddressTxResource", "GET_ADDRESS")
    logger.info({"RequestType": request_type, "ContactId": contact_id})
    if request_type.upper() == "GET_ADDRESS":
        tn = contact_data["CustomerEndpoint"]["Address"]
        zip_code = parameters.get("ZipCodeHint", None)
        data = {"phone": tn}
        if zip_code:
            data["zip_code"] = zip_code

        data = identity.get_address(address_lookup, data)

        # https://docs.aws.amazon.com/connect/latest/adminguide/connect-lambda-functions.html
        # The output returned from the function must be a flat object of
        # key/value pairs, with values that include only alphanumeric,
        # dash, and underscore characters.
        # Nested and complex objects are not supported. The size of the
        # returned data must be less than 32 Kb of UTF-8 data.
        # Because of this we flatten the response with the first address
        data = identity.flatten_address_data(data)

    elif request_type.upper() in ("CONFIRM_ADDRESS", "CLOSE_ADDRESS_TX"):
        url = parameters.get("ConfirmUrl") or parameters.get("CloseUrl")
        data = identity.finalize_tx(address_lookup, url)

    else:
        raise ValueError(
            f"AddressTxResource type: {request_type} is unsupported"
        )

    logger.debug(data)
    data["data_source"] = "identity"

    return data
