# Owner: Rajasakthiyan.G
# Email: rajasakthiyan.g@gmail.com

import json
import os
import boto3

client = boto3.client("dynamodb")
BEARER_TOKEN = os.environ["BEARER_TOKEN"]


def authorization_handler(event, context):
    """
    Lambda handler that performing authorization.
    The name of the table is 'TABLE_NAME' from enviornment
    """
    token = event["headers"]["Authorization"]
    if BEARER_TOKEN == token:
        return {
            "principalId": "authenticated",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["methodArn"],
                    }
                ],
            },
        }
    else:
        return {
            "principalId": "unauthenticated",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Deny",
                        "Resource": event["methodArn"],
                    }
                ],
            },
        }
