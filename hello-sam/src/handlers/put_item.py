# Owner: Rajasakthiyan.G
# Email: rajasakthiyan.g@gmail.com

import json
import os
import boto3

client = boto3.client("dynamodb")

EXPECTED_KEYS = ("id", "Weather")
TABLE_NAME = os.environ["TABLE_NAME"]


class InvalidRequestError(Exception):
    """
    Custom exception for capturing unknown keys present in given request body.
    """

    def __str__(self) -> str:
        return "'id' and 'Weather' are the only attributes in the request body, contains other attributes"


class MissingKeyError(Exception):
    """
    Custom exception for capturing missing keys.
    """

    def __init__(self, missing_key: str, *args: object) -> None:
        self.missing_key = missing_key
        super().__init__(*args)

    def __str__(self) -> str:
        return "'${self.missing_key}' is missing. 'id' and 'Weather' attributes should be present in the request body"


def validate_expected_data(data):
    """
    Validate expected keys in EXPECTED_KEYS.
    """
    for key in EXPECTED_KEYS:
        if not key in data:
            raise MissingKeyError(key)


def validate_valid_data(data):
    """
    Validate the data with number of keys in EXPECTED_KEYS.
    """
    if not len(data) == len(EXPECTED_KEYS):
        raise InvalidRequestError()


def put_item_handler(event, context):
    """
    Lambda handler that performing validation and put call to DynamoDB.
    The name of the table is 'TABLE_NAME' from enviornment
    """
    try:
        body = json.loads(event["body"])
        validate_expected_data(body)
        validate_valid_data(body)
        id, weather = body["id"], body["Weather"]
        result = client.put_item(
            TableName=TABLE_NAME,
            Item={"id": {"S": id}, "Weather": {"S": weather}},
        )
        return {"statusCode": 200, "body": json.dumps(result)}
    except (MissingKeyError, InvalidRequestError) as error:
        return {"statusCode": 400, "body": {"error": str(error)}}
