import boto3

brt = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def bedrock_streaming_invoke(body, model_id):
    response = brt.invoke_model_with_response_stream(
        modelId=model_id, 
        body=body, 
    )
    return response.get('body')