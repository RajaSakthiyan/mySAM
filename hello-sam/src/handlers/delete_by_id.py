# Owner: Rajasakthiyan.G
# Email: rajasakthiyan.g@gmail.com

import json
import os
import boto3

client = boto3.client("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]


def delete_by_id_handler(event, context):
    """
    Lambda handler that performing delete call to DynamoDB.
    The name of the table is 'TABLE_NAME' from enviornment
    """
    id = event["pathParameters"]["id"]
    client.delete_item(TableName=TABLE_NAME, Key={"id": {"S": str(id)}})

    response = {"statusCode": 202, "body": None}

    return response
