import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('products')

def handler(event, context):
    '''
    Provide an event that contains the following keys:
    
    - operation: one of the operations in the operations dict below
    - payload: a JSON object containing parameters to pass to the operation being performed
    '''
    
    def db_create(x):
        table.put_item(**x)
    
    def db_get(id):
        response = table.get_item(Key=id)
        return response
    
    def db_get_all(x):
        response = table.scan()
        return response['Items']

    def echo(x):
        return x

    operation = event['operation']
    
    operations = {
        'create': db_create,
        'get': db_get,
        'getAll': db_get_all,
        'echo': echo # for debugging purposes
    }
    
    if operation in operations:
        return operations[operation](event.get('payload'))
    else:
        raise ValueError(f"Unrecognized operation: {operation}")
    
