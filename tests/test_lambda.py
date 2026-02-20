import json
import os
import boto3
from moto import mock_aws

from src.lambda_function import lambda_handler


@mock_aws
def test_lambda_returns_count():
    # Ensure Lambda uses the same table name we create in the test
    os.environ["TABLE_NAME"] = "resume-visitor-api"
    os.environ["COUNTER_ID"] = "visitors"
    os.environ["AWS_REGION"] = "eu-north-1"
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")

    table = dynamodb.create_table(
        TableName="resume-visitor-api",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()

    response = lambda_handler({}, {})
    print("LAMBDA_RESPONSE:", response)

    assert response["statusCode"] == 200

    body = json.loads(response["body"])
    assert body["count"] == 1


@mock_aws
def test_lambda_increments_count():
    import os
    import boto3
    import json
    from src.lambda_function import lambda_handler

    os.environ["TABLE_NAME"] = "resume-visitor-api"
    os.environ["COUNTER_ID"] = "visitors"
    os.environ["AWS_REGION"] = "eu-north-1"

    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
    table = dynamodb.create_table(
        TableName="resume-visitor-api",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()

    r1 = lambda_handler({}, {})
    c1 = json.loads(r1["body"])["count"]

    r2 = lambda_handler({}, {})
    c2 = json.loads(r2["body"])["count"]

    assert r1["statusCode"] == 200
    assert r2["statusCode"] == 200
    assert c2 == c1 + 1
