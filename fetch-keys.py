import boto3
import os
import StringIO
import sys
from subprocess import call

client = boto3.client('dynamodb')

port = os.environ['PORT']
table = os.environ['KEY_TABLE']
application = os.environ['APPLICATION']
service = os.environ['SERVICE']
home = os.environ['HOME']
response = None

try:
    response = client.query(
        TableName=table,
        KeyConditionExpression='Application_Service = :applicationServiceName',
        ExpressionAttributeValues={
            ':applicationServiceName': {
                'S': application + '#' + service
            }
        },
        ConsistentRead=True
    )
except Exception as problem:
    print 'DynamoDb Query Error'
    sys.exit()

def combineHostStrings(lastOne, nextOne):
    return lastOne + ' ' + nextOne

def mapItemsToHostStrings(item):
    return item['Host_Port']['S']

if len(response['Items']) > 0:
    command = 'hamba reconfigure ' + port + ' ' + reduce(combineHostStrings, map(mapItemsToHostStrings, response['Items']))
    oldConfig = ''

    try:
        with open(home + '/.config', 'r') as myfile:
            oldConfig = myfile.read()
    except Exception as problem:
        print 'Exception, likely no config file'

    if oldConfig != command:
        print command
        try:
            with open(home + '/.config', 'w') as myfile:
                myfile.write(command)
        except Exception as problem:
            print 'Exception, likely error writing file'
        call(command.split(' '))
else:
    print "No config :("
