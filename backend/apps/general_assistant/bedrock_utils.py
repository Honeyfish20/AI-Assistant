import json
import boto3


def bedrock_streaming_invoke(body, model_id, model_region):
    brt = boto3.client(
                service_name='bedrock-runtime', 
                region_name=model_region,
    )
    response = brt.invoke_model_with_response_stream(
        modelId=model_id, 
        body=body, 
    )
    return response

def bedrock_streaming(response):
    msg = ""
    for chunk in response.get('body'):
        if 'amazon-bedrock-invocationMetrics' in json.loads(chunk.get('chunk').get('bytes').decode()):
            invoke_matrics = json.loads(chunk.get('chunk').get('bytes').decode())['amazon-bedrock-invocationMetrics']
        if 'delta' in json.loads(chunk.get('chunk').get('bytes').decode()):
            if 'text' in json.loads(chunk.get('chunk').get('bytes').decode())['delta']:
                extracted_text = json.loads(chunk.get('chunk').get('bytes').decode())['delta']['text']
                msg += extracted_text
    return msg

def chat(system_prompt, messages, model_id, model_region, max_tokens, stop_sequences, temperature, ):
    body = json.dumps({
            'system': system_prompt,
            'messages': messages,
            'max_tokens': max_tokens,
            'stop_sequences': stop_sequences.split(';') if ';' in stop_sequences else [],
            'temperature': temperature,
            "anthropic_version": "" 
            })
    response = bedrock_streaming_invoke(body, model_id, model_region)
    msg = bedrock_streaming(response)
    return msg

async def bedrock_streaming_feishu(response, sender, message_id):
    msg = ""
    one_streaming_limit = 15
    temp_len = 0
    for chunk in response.get('body'):
        if 'amazon-bedrock-invocationMetrics' in json.loads(chunk.get('chunk').get('bytes').decode()):
            invoke_matrics = json.loads(chunk.get('chunk').get('bytes').decode())['amazon-bedrock-invocationMetrics']
        if 'delta' in json.loads(chunk.get('chunk').get('bytes').decode()):
            if 'text' in json.loads(chunk.get('chunk').get('bytes').decode())['delta']:
                extracted_text = json.loads(chunk.get('chunk').get('bytes').decode())['delta']['text']
                msg += extracted_text
                temp_len += len(extracted_text)
                if temp_len > one_streaming_limit:
                    await sender.update_card(msg + "🚀生成中...", message_id)
                    temp_len = 0
    await sender.update_card(msg, message_id)
                
async def streaming_chat_feishu(system_prompt, messages, model_id, model_region, max_tokens, stop_sequences, temperature, sender, user_id):
    card_message_id = await sender.get_card_id(user_id)    
    body = json.dumps({
            'system': system_prompt,
            'messages': messages,
            'max_tokens': max_tokens,
            'stop_sequences': stop_sequences.split(';') if ';' in stop_sequences else [],
            'temperature': temperature,
            "anthropic_version": "" 
            })
    response = bedrock_streaming_invoke(body, model_id, model_region) 
    await bedrock_streaming_feishu(response, sender, card_message_id)
    
    
