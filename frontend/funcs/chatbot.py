import json
import boto3
from botocore.client import Config
import streamlit as st

class Chatbot:
    def __init__(self):
        pass
        
    def bedrock_streaming_invoke(self, body, model_id, region_name):
        brt = boto3.client(
            service_name='bedrock-runtime', 
            region_name=region_name
            )
        response = brt.invoke_model_with_response_stream(
            modelId=model_id, 
            body=body, 
        )
        return response
    
    def bedrock_kb_invoke(self, query_list, knowledgeBaseId, region_name):
        bedrock_config = Config(connect_timeout=1200, read_timeout=1200, retries={'max_attempts': 4})
        client = boto3.client('bedrock-agent-runtime', region_name=region_name, config=bedrock_config)
        knowledge_chunks = []
        for query_item in query_list:
            response = client.retrieve(
                knowledgeBaseId=knowledgeBaseId,
                retrievalQuery={
                    'text': query_item
                },
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': 2
                    }
                },
                nextToken='string'
            )
            for item in response["retrievalResults"]:
                knowledge_chunks.append(item['content']['text'])
        return knowledge_chunks
    
    def bedrock_streaming_st_show(self, response):
        msg = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            for chunk in response.get('body'):
                if 'amazon-bedrock-invocationMetrics' in json.loads(chunk.get('chunk').get('bytes').decode()):
                    invoke_matrics = json.loads(chunk.get('chunk').get('bytes').decode())['amazon-bedrock-invocationMetrics']
                if 'delta' in json.loads(chunk.get('chunk').get('bytes').decode()):
                    if 'text' in json.loads(chunk.get('chunk').get('bytes').decode())['delta']:
                        msg += json.loads(chunk.get('chunk').get('bytes').decode())['delta']['text']
                        message_placeholder.markdown(msg + "|")
                message_placeholder.markdown(msg + "|")
            message_placeholder.markdown(msg)
        return msg

    def bedrock_streaming(self, response):
        msg = ""
        for chunk in response.get('body'):
            if 'amazon-bedrock-invocationMetrics' in json.loads(chunk.get('chunk').get('bytes').decode()):
                invoke_matrics = json.loads(chunk.get('chunk').get('bytes').decode())['amazon-bedrock-invocationMetrics']
            if 'delta' in json.loads(chunk.get('chunk').get('bytes').decode()):
                if 'text' in json.loads(chunk.get('chunk').get('bytes').decode())['delta']:
                    msg += json.loads(chunk.get('chunk').get('bytes').decode())['delta']['text']
        return msg