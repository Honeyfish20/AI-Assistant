import json
import streamlit as st

from .chatbot import Chatbot


class QCChatbot(Chatbot):
    def __init__(self, qc_chat_name, qc_chat_background, dialogue_checkers):
        super().__init__()
        # Chat Name
        self.qc_chat_name = qc_chat_name
        # Background Information of the Role Chatbot
        self.qc_chat_background = qc_chat_background
        # Skills the role chatbot can use
        self.dialogue_checkers = dialogue_checkers
    
    def bedrock_streaming_chat(self, dialogue_checker, history_messages):
        
        if dialogue_checker.query_list_generation_prompt is None:
            body = json.dumps({
                    'system': '',
                    'messages': [{"role": "user", "content": dialogue_checker.dialogue_checker_prompt.format(msg=history_messages)}],
                    'max_tokens': dialogue_checker.llm.max_tokens,
                    'stop_sequences': dialogue_checker.llm.stop_sequences.split(';') if ';' in dialogue_checker.llm.stop_sequences else [],
                    'temperature': dialogue_checker.llm.temperature,
                    "anthropic_version": "" 
                    })
            response = self.bedrock_streaming_invoke(body, dialogue_checker.llm.model_id, dialogue_checker.llm.region)
            msg = self.bedrock_streaming(response)
            msg = json.loads(msg)
        else:
            body = json.dumps({
                    'system': '',
                    'messages': [{"role": "user", "content": dialogue_checker.query_list_generation_prompt.format(msg=history_messages)}],
                    'max_tokens': dialogue_checker.llm.max_tokens,
                    'stop_sequences': dialogue_checker.llm.stop_sequences.split(';') if ';' in dialogue_checker.llm.stop_sequences else [],
                    'temperature': dialogue_checker.llm.temperature,
                    "anthropic_version": "" 
                    })
            response = self.bedrock_streaming_invoke(body, dialogue_checker.llm.model_id, dialogue_checker.llm.region)
            query_list = self.bedrock_streaming(response)
            query_list = json.loads(query_list)
            st.write('Query List: {}. Begin searching'.format(str(query_list)))
            knowledge_chunks = self.bedrock_kb_invoke(query_list, dialogue_checker.knowledge_base_id, dialogue_checker.llm.region)
            
            
            body = json.dumps({
                    'system': '',
                    'messages': [{"role": "user", "content": dialogue_checker.dialogue_checker_prompt.format(msg=history_messages, knowledge=str(knowledge_chunks))}],
                    'max_tokens': dialogue_checker.llm.max_tokens,
                    'stop_sequences': dialogue_checker.llm.stop_sequences.split(';') if ';' in dialogue_checker.llm.stop_sequences else [],
                    'temperature': dialogue_checker.llm.temperature,
                    "anthropic_version": "" 
                    })
            response = self.bedrock_streaming_invoke(body, dialogue_checker.llm.model_id, dialogue_checker.llm.region)
            msg = self.bedrock_streaming(response)
            msg = json.loads(msg)
            msg["knowledge_chunks"] = knowledge_chunks
        return msg
