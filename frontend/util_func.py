import streamlit as st
import requests
import json
import boto3
from funcs.role_chatbot import RoleChatbot
from funcs.QC_chatbot import QCChatbot
from funcs.components.skill import Skill
from funcs.components.checker import Checker
from funcs.components.dialogue_checker import DialogueChecker
from pathlib import Path
import base64
import os
import re

############### Funcs ###############

def markdown_images(markdown):
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'

    return img_html


def markdown_insert_images(markdown):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if os.path.exists(image_path):
            markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown

def get_token(username='tonyhh', password='tonyhh', url='http://127.0.0.1:8501/api/token/'):
    payload = {
        "username": username,
        "password": password
        }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    token = json.loads(response.content)['access']
    return token

def get_role_chatbots(token, url='http://127.0.0.1:8501/api/role_chatbot/'):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()

def get_quality_check_chatbots(token, url='http://127.0.0.1:8501/api/quality_check_chatbots/'):
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()

def get_core_prompts_by_id(token, id, url='http://127.0.0.1:8501/api/core_prompts/'):
    url = url + str(id) + '/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()

def get_skill_by_id(token, id, url='http://127.0.0.1:8501/api/skill/'):
    url = url + str(id) + '/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()

def get_checker_by_id(token, id, url='http://127.0.0.1:8501/api/checker/'):
    url = url + str(id) + '/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()

def get_model_by_id(token, id, url='http://127.0.0.1:8501/api/base_models/'):
    url = url + str(id) + '/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()['model_id']

def get_model_region_by_id(token, id, url='http://127.0.0.1:8501/api/base_models/'):
    url = url + str(id) + '/'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    response =requests.get(url, headers=headers)
    return response.json()['region']

def streaming_invoke(body, model_id):
    brt = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

    response = brt.invoke_model_with_response_stream(
        modelId=model_id, 
        body=body, 
    )
    return response

def get_next_version(version_choicer):
    version_int = int(version_choicer[1:])
    return 'v' + str(version_int+1)

def create_role_chatbot(token, data):
    checkers = {}
    for checker_data in [checker for skill in data['skills'] for checker in skill.get('skill_checkers', [])]:
        checker = Checker(
            checker_data['checker_name'],
            checker_data['checker_description'],
            checker_data['checker_prompt'],
            checker_data['checker_time_limit'],
            get_model_by_id(token, checker_data['model_id']),
            checker_data['max_tokens'],
            checker_data['stop_sequences'],
            checker_data['temperature'],
            get_model_region_by_id(token, checker_data['model_id'])
        )
        checkers[checker_data['id']] = checker

    skills = []
    for skill_data in data['skills']:
        skill_checkers = [checkers[checker_id] for checker_id in [checker['id'] for checker in skill_data.get('skill_checkers', [])]]
        skill = Skill(
            skill_data['skill_name'],
            skill_data['skill_description'],
            skill_data['skill_examples'],
            skill_checkers,
            get_model_by_id(token, skill_data['model_id']),
            skill_data['max_tokens'],
            skill_data['stop_sequences'],
            skill_data['temperature'],
            get_model_region_by_id(token, skill_data['model_id'])
        )
        skills.append(skill)

    role_chatbot = RoleChatbot(
        data['role_name'],
        data['role_background'],
        data['chat_background'],
        data['language_styles'],
        skills,
        data['system_prompt']['prompt']
    )

    return role_chatbot

def create_quality_check_chatbot(token, data):
    # 提取 chatbot 名称和背景信息
    qc_chat_name = data.get("qc_chat_name")
    qc_chat_background = data.get("qc_chat_background")
    
    # 创建 DialogueChecker 实例列表
    dialogue_checkers = []
    for checker_data in data.get("dialogue_checkers", []):
        dialogue_checker = DialogueChecker(
            dialogue_checker_name=checker_data.get("dialogue_checker_name"),
            dialogue_checker_description=checker_data.get("dialogue_checker_description"),
            dialogue_checker_prompt=checker_data.get("dialogue_checker_prompt"),
            model_id=get_model_by_id(token, checker_data.get("model_id")),
            max_tokens=checker_data.get("max_tokens", 8192),
            stop_sequences=checker_data.get("stop_sequences", []),
            temperature=checker_data.get("temperature", 0),
            region=get_model_region_by_id(token, checker_data.get("model_id"))
        )
        dialogue_checkers.append(dialogue_checker)
    for checker_data in data.get("knowledge_base_dialogue_checkers", []):
        knowledge_base_dialogue_checker = DialogueChecker(
            dialogue_checker_name=checker_data.get("knowledge_base_dialogue_checker_name"),
            dialogue_checker_description=checker_data.get("knowledge_base_dialogue_checker_description"),
            dialogue_checker_prompt=checker_data.get("knowledge_base_dialogue_checker_prompt"),
            query_list_generation_prompt=checker_data.get("query_list_generation_prompt"),
            knowledge_base_id=checker_data.get("knowledge_base_id"),
            model_id=get_model_by_id(token, checker_data.get("model_id")),
            max_tokens=checker_data.get("max_tokens", 8192),
            stop_sequences=checker_data.get("stop_sequences", []),
            temperature=checker_data.get("temperature", 0),
            region=get_model_region_by_id(token, checker_data.get("model_id"))
        )
        dialogue_checkers.append(knowledge_base_dialogue_checker)
    
    # 创建 QCChatbot 实例
    qc_chatbot = QCChatbot(
        qc_chat_name=qc_chat_name,
        qc_chat_background=qc_chat_background,
        dialogue_checkers=dialogue_checkers
    )
    
    return qc_chatbot

def get_zh_readme(path='./readme/user_readme_zh.md'):
    with open(path, "r") as f:
        markdown_content = f.read()
    st.markdown(markdown_insert_images(markdown_content), unsafe_allow_html=True)
    
def get_en_readme(path='./readme/user_readme_en.md'):
    with open(path, "r") as f:
        markdown_content = f.read()
    st.markdown(markdown_insert_images(markdown_content), unsafe_allow_html=True)
############### Funcs ###############