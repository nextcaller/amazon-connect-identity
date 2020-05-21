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
    attributes_data = contact_data["Attributes"] if contact_data else {}
    contact_id = contact_data["ContactId"]

    request_type = attributes_data.get("AddressTxResource", "")
    logger.info({"RequestType": request_type, "ContactId": contact_id})
    if request_type.upper() == "GET_ADDRESS":
        tn = contact_data["CustomerEndpoint"]["Address"]
        zip_code = attributes_data.get("ZipCodeHint", None)
        data = {"phone": tn}
        if zip_code:
            data["zip_code"] = zip_code

        data = identity.get_address(address_lookup, data)
        data = json.dumps(data)

    elif request_type.upper() == "CONFIRM_ADDRESS":
        confirm_url = attributes_data["ConfirmUrl"]
        data = identity.confirm_address(address_lookup, confirm_url)
        data = json.dumps(data)

    elif request_type.upper() == "CLOSE_ADDRESS_TX":
        close_url = attributes_data["CloseUrl"]
        data = identity.close_address_tx(address_lookup, close_url)
        data = json.dumps(data)
    else:
        raise ValueError(
            f"AddressTxResource type: {request_type} is unsupported"
        )

    return data
