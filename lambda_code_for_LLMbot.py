import json
import boto3

boto3_bedrock_stuff = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    print(event)

    try:
        # Attempt to parse the 'body' string as JSON
        body = json.loads(event.get('body', '{}'))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format in the body'}),
        }

    # Retrieve 'prompt' from the parsed JSON
    user_prompt = body.get('prompt', '')

    # Check if 'prompt' field is present and non-empty
    if not user_prompt:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing or invalid prompt in the request'}),
        }

    modelId = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    contentType = 'application/json'

    response = boto3_bedrock_stuff.invoke_model_with_response_stream(
        body=json.dumps({
            "inputText": user_prompt,
            "textGenerationConfig": {
                "maxTokenCount": 20,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        }), modelId=modelId, accept=accept, contentType=contentType)

    # Process the response from the model
    response_body = b''  # Initialize an empty bytes object
    stream = response.get('body')

    if 'body' in response:
        stream = response['body']

        for event in stream:
            chunk = event.get('chunk')
            if chunk:
                response_body += chunk.get('bytes')

    try:
        # Parse the complete response body
        response_data = json.loads(response_body.decode())
    except json.JSONDecodeError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to parse the model response'}),
        }

    # Include relevant information in the response
    return {
        'statusCode': 200,
        'body': json.dumps({'success': True, 'outputText': response_data.get('outputText', '')}),
    }