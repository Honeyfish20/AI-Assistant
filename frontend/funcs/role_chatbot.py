from .chatbot import Chatbot
from .components.skill import Skill
from .components.checker import Checker

import json
import streamlit as st

class RoleChatbot(Chatbot):
    def __init__(self, role_name, role_background, conversation_background, language_styles, skills, system_prompt):
        super().__init__()
        # Role Name
        self.role_name = role_name
        # Background Information of the Role Chatbot
        self.role_background = role_background
        self.conversation_background = conversation_background
        # Few shots of role to simulate the language style
        self.language_styles = language_styles
        # Skills the role chatbot can use
        self.skills = skills
        # system prompt
        self.system_prompt = system_prompt
    
    def create_skill(self, skill_name, skill_description, skill_examples, skill_checker, model_id, max_tokens=8192, stop_sequences=[], temperature=0):
        self.skills.append(
            Skill(skill_name, skill_description, skill_examples, skill_checker, model_id, max_tokens, stop_sequences, temperature)
        )
        
    def create_checker(self, checker_name, checker_description, checker_prompt, model_id, max_tokens=8192, stop_sequences=[], temperature=0):
        self.skills.append(
            Skill(checker_name, checker_description, checker_prompt, model_id, max_tokens, stop_sequences, temperature)
        )
    
    def bedrock_streaming_chat(self, skill, history_messages, checker=None):
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
        if skill.skill_checker == "None" or len(skill.skill_checker)==0:
            # if output of the skill doesn't need to be checked
            msg = self.bedrock_streaming(response)
        else:
            # if output of the skill need to be checked then response
            msg = self.bedrock_streaming(response)
            check_result = self.check(msg, checker)
            st.write(check_result)
            error_msg = []
            error_reason = []
            limit = checker.checker_time_limit
            while int(check_result["result"]) == 0 and limit > 0:
                limit -= 1
                error_msg.append(msg)
                error_reason.append(check_result["reason"])
                completed_system_prompt = self.system_prompt.format(
                    role_background=self.role_background,
                    chat_background=self.conversation_background,
                    conversation_examples=self.language_styles,
                    skill_name=skill.skill_name,
                    skill_description=skill.skill_description,
                    skill_examples=skill.skill_examples,
                    error_msg=str(error_msg),
                    error_reason=str(error_reason)
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
                msg = self.bedrock_streaming(response)
                check_result = self.check(msg, checker)
        return msg
        
    def check(self, msg, checker):
        body = json.dumps({
                'system': '',
                'messages': [{"role": "user", "content": checker.checker_prompt.format(msg=msg)}],
                'max_tokens': checker.llm.max_tokens,
                'stop_sequences': checker.llm.stop_sequences.split(';') if ';' in checker.llm.stop_sequences else [],
                'temperature': checker.llm.temperature,
                "anthropic_version": "" 
                })
        response = self.bedrock_streaming_invoke(body, checker.llm.model_id, checker.llm.region)
        check_result = json.loads(self.bedrock_streaming(response))
        return check_result      