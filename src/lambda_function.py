import json
import os
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("TABLE_NAME", "resume-visitor-api")
COUNTER_ID = os.environ.get("COUNTER_ID", "visitors")


def build_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "content-type",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    # Create the DynamoDB resource at runtime (important for moto tests)
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION", "eu-north-1"))
    table = dynamodb.Table(TABLE_NAME)

    try:
        result = table.update_item(
            Key={"id": COUNTER_ID},
            UpdateExpression="ADD #c :inc",
            ExpressionAttributeNames={"#c": "count"},
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )

        new_count = int(result["Attributes"]["count"])
        return build_response(200, {"count": new_count})

    except ClientError as e:
        return build_response(500, {"error": str(e)})
