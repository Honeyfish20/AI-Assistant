class RoleChatbot(Chatbot):
    def bedrock_streaming_chat_iter(self, skill, history_messages, checker=None):
        """迭代器版本的流式聊天"""
        completed_system_prompt = self.system_prompt.format(
            role_background=self.role_background,
            chat_background=self.conversation_background,
            conversation_examples=self.language_styles,
            skill_name=skill.skill_name,
            skill_description=skill.skill_description,
            skill_examples=skill.skill_examples,
            error_msg='暂无',
            error_reason='暂无'
        )
        
        body = json.dumps({
            'system': completed_system_prompt,
            'messages': history_messages,
            'max_tokens': skill.llm.max_tokens,
            'stop_sequences': skill.llm.stop_sequences.split(';') if ';' in skill.llm.stop_sequences else [],
            'temperature': skill.llm.temperature,
            "anthropic_version": "" 
        })
        
        response = self.bedrock_streaming_invoke(body, skill.llm.model_id, skill.llm.region)
        
        for chunk in response.get('body'):
            if 'delta' in json.loads(chunk.get('chunk').get('bytes').decode()):
                if 'text' in json.loads(chunk.get('chunk').get('bytes').decode())['delta']:
                    yield json.loads(chunk.get('chunk').get('bytes').decode())['delta']['text'] 