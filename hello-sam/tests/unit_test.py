import json
from pathlib import Path
import boto3
import os
from moto import mock_dynamodb
import pytest
import yaml
import src.handlers.put_item as put_item


@pytest.fixture(scope="module")
def sam_template(sam_template_path: str = "../template.yaml") -> dict:
    """
    Utility Function to read the SAM template for the current project and put this fixture as module scoped.
    """
    with Path(sam_template_path).open("r") as fp:
        template = fp.read().replace("!", "")
        return yaml.safe_load(template)


@pytest.fixture
@mock_dynamodb
def dynamodb(scope="module"):
    """Create an dynamodb table and return the table object"""
    return boto3.client("dynamodb").create(
        **sam_template["Resources"]["DynamoDBTable"]["Properties"]
    )


@pytest.fixture(autouse=True)
def setup_and_teardown(sam_template):
    os.environ["TABLE_NAME"] = sam_template["Resources"]["DynamoDBTable"]["Properties"][
        "TableName"
    ]
    yield
    del os.environ["TABLE_NAME"]


def test_success_put_item():
    """Test the custom s3 ls function mocking S3 with moto"""
    print("-" * 10 + os.environ["TABLE_NAME"])
    request_data = json.dumps({"id": "1", "Weather": "cold"})
    response = put_item.put_item_handler({"body": request_data}, None)
    assert response["statusCode"] == 200


def test_invalid_put_item():
    """Test the custom s3 ls function mocking S3 with moto"""
    print("-" * 10 + os.environ["TABLE_NAME"])
    request_data = json.dumps({"id": "1", "Weather": "cold", "whoAmI": "???"})
    response = put_item.put_item_handler({"body": request_data}, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "error": str(put_item.InvalidRequestError())
    }


def test_missing_put_item():
    """Test the custom s3 ls function mocking S3 with moto"""
    print("-" * 10 + os.environ["TABLE_NAME"])
    request_data = json.dumps({"id": "1"})
    response = put_item.put_item_handler({"body": request_data}, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "error": str(put_item.MissingKeyError("Weather"))
    }
