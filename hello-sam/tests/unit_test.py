import json
from pathlib import Path
import boto3
from boto3.dynamodb.conditions import Key
import os
from moto import mock_dynamodb
import pytest
import yaml

import sys

sys.path.append(str(Path(Path.cwd(), "../src/handlers")))
import put_item


@pytest.fixture(scope="module")
def sam_template(sam_template_path: str = "../template.yaml") -> dict:
    """
    Utility Function to read the SAM template for the current project and put this fixture as module scoped.
    """
    with Path(sam_template_path).open("r") as fp:
        template = fp.read().replace("!", "")
        return yaml.safe_load(template)


@pytest.fixture
def dynamodb_table(sam_template):
    """Create an dynamodb table and yeild the table object for further mocking"""
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.create_table(
            **sam_template["Resources"]["DynamoDBTable"]["Properties"]
        )
        yield table


@pytest.fixture(autouse=True)
def setup_and_teardown(sam_template):
    """Fixture for set-up and tear down TABLE_NAME from environment variable"""
    os.environ["TABLE_NAME"] = sam_template["Resources"]["DynamoDBTable"]["Properties"][
        "TableName"
    ]
    yield
    del os.environ["TABLE_NAME"]


def test_success_put_item(dynamodb_table):
    """Test successful put item"""
    request_data = {"id": "1", "Weather": "cold"}
    response = put_item.put_item_handler({"body": json.dumps(request_data)}, None)
    assert response["statusCode"] == 200
    item = dynamodb_table.get_item(Key={"id": "1"})
    assert item["Item"]["id"] == request_data["id"]
    assert item["Item"]["Weather"] == request_data["Weather"]


def test_invalid_put_item(dynamodb_table):
    """Test failure put item when new key present in the payload"""
    print("-" * 10 + os.environ["TABLE_NAME"])
    request_data = json.dumps({"id": "2", "Weather": "hot", "whoAmI": "???"})
    response = put_item.put_item_handler({"body": request_data}, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "error": str(put_item.InvalidRequestError())
    }
    item = dynamodb_table.get_item(Key={"id": "1"})
    assert item.get("Item") == None


def test_missing_put_item(dynamodb_table):
    """Test failure put item when Weather is missing in the payload"""
    print("-" * 10 + os.environ["TABLE_NAME"])
    request_data = json.dumps({"id": "3"})
    response = put_item.put_item_handler({"body": request_data}, None)
    assert response["statusCode"] == 400
    assert json.loads(response["body"]) == {
        "error": str(put_item.MissingKeyError("Weather"))
    }
    item = dynamodb_table.get_item(Key={"id": "1"})
    assert item.get("Item") == None
