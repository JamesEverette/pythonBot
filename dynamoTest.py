import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

dynamoTableName = os.environ.get('dynamoTableName')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(dynamoTableName)


#print(dynamodb.list_tables())
#print(table)
output = table.get_item(
    Key={
        'CrashNumber':1,
        'CrashLevel':1})

print(output)
