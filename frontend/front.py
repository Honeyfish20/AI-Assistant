import streamlit as st
import os
import logging
from configs.system_cfg import cfg_LLM_kwargs, cfg_modes
from funcs.role_chatbot import RoleChatbot
from funcs.QC_chatbot import QCChatbot
from funcs.components.skill import Skill
from funcs.components.checker import Checker
from funcs.components.dialogue_checker import DialogueChecker
import time
from copy import deepcopy
import re
import json
from datetime import datetime
import threading
from tqdm import tqdm
import boto3
import json
import pickle
import requests

from util_func import get_token, get_role_chatbots, get_quality_check_chatbots, \
    get_core_prompts_by_id, get_skill_by_id, get_checker_by_id, streaming_invoke, \
        get_next_version, create_role_chatbot, create_quality_check_chatbot, get_zh_readme, \
            get_en_readme


############### system config ###############
def traverse_config_pickle_files(directory):
    pickle_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pickle'):
                pickle_files[file[:-7]] = os.path.join(root, file)
    return pickle_files

st.set_page_config(page_title="Smart Training Assistant - AWS GenAIIC", page_icon="🚀")
token = get_token()
role_chatbots = get_role_chatbots(token)
quality_check_chatbots = get_quality_check_chatbots(token)
############### system config ###############


############### UI ###############
with st.sidebar:
    st.title('AWS GenAIIC')
    st.write('Smart Training Assistant build by AWS GenAIIC GCR Team. Feel free to contact Hao Huang (tonyhh@amazon.com) if you have any questions!')

    mode_choicer = st.selectbox(label="Mode",
                                options=cfg_modes.keys(), 
                                key="mode_choicer",
                                index=0, 
                                label_visibility="visible",
                                )
    if mode_choicer == "Readme":
        readme_language_choicer = st.selectbox(label="language",
                                    options=['English', 'Chinese'], 
                                    key="language_choicer",
                                    index=0, 
                                    label_visibility="visible",)
        
    if mode_choicer == "Role Assistant":
        role_chatbots_name = [item['role_name'] for item in role_chatbots]
        role_chat_choicer = st.selectbox(label="Role Choicer",
                                    options=role_chatbots_name, 
                                    key="role_chat_choicer",
                                    index=0, 
                                    label_visibility="visible",)
        role_chat_index = role_chatbots_name.index(role_chat_choicer)
        role_chatbot = role_chatbots[role_chat_index]
        role_chatbot_used = create_role_chatbot(token, role_chatbot)
        
        skills = role_chatbot['skills']
        skills_name = [item['skill_name'] for item in skills]
        skill_choicer = st.selectbox(label="Skill Choicer",
                                    options=skills_name, 
                                    key="config_choicer",
                                    index=0, 
                                    label_visibility="visible",)
        skill_index = skills_name.index(skill_choicer)
        skill_used = role_chatbot_used.skills[skill_index]
        
        checker_used = None
        if len(role_chatbot['skills'][skill_index]['skill_checkers']) > 0:
            checkers_name = [item['checker_name'] for item in role_chatbot['skills'][skill_index]['skill_checkers']]
            checker_choicer = st.selectbox(label="Checker Choicer",
                                        options=checkers_name, 
                                        key="checker_choicer_disabled",
                                        index=0,
                                        label_visibility="visible")
            checker_index = checkers_name.index(checker_choicer)
            checker_used = skill_used.skill_checker[checker_index]
        
        clear_button = st.button(label="Clear All", key="clear_chat")

    if mode_choicer == "Dialogue Check Assistant":
        quality_check_chatbots_name = [item['qc_chat_name'] for item in quality_check_chatbots]
        config_choicer = st.selectbox(label="Config Choicer",
                                    options=quality_check_chatbots_name, 
                                    key="config_choicer",
                                    index=0, 
                                    label_visibility="visible")
        dialogue_uploaded_file = st.file_uploader(label="Upload Dialogue", type='txt')
        quality_check_chatbot_index = quality_check_chatbots_name.index(config_choicer)
        quality_check_chatbot = quality_check_chatbots[quality_check_chatbot_index]
        quality_check_chatbot_used = create_quality_check_chatbot(token, quality_check_chatbot)
            
        dialogue_checkers_name = [item.dialogue_checker_name for item in quality_check_chatbot_used.dialogue_checkers]
        dialogue_checker_choicer = st.selectbox(label="Dialogue Checkers",
                                    options=dialogue_checkers_name, 
                                    key="dialogue_checker",
                                    index=0,
                                    label_visibility="visible")
        dialogue_checker_index = dialogue_checkers_name.index(dialogue_checker_choicer)
        dialogue_checker_used = quality_check_chatbot_used.dialogue_checkers[dialogue_checker_index]
        check_button = st.button(label="Check Dialogue", key="check_button")
        clear_button = st.button(label="Clear All", key="clear_chat")

# st.title("Smart Training Assistant")
############### UI ###############


############### Logic ###############
if mode_choicer == "Readme":
    if readme_language_choicer == "English":
        get_en_readme()
    if readme_language_choicer == "Chinese":
        get_zh_readme()

if mode_choicer == "Role Assistant":
    if clear_button:
        st.session_state['user'] = []
        st.session_state['assistant'] = []
        st.session_state.messages = []
        st.experimental_rerun()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)  
        msg = role_chatbot_used.bedrock_streaming_chat(skill_used, st.session_state.messages, checker_used)
        with st.chat_message("assistant"):
            st.write(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})

if mode_choicer == "Dialogue Check Assistant":
    if clear_button:
        st.session_state['user'] = []
        st.session_state['assistant'] = []
        st.session_state.messages = []
        st.experimental_rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if dialogue_uploaded_file:
        lines = dialogue_uploaded_file.getvalue().decode('utf-8').split('\n')
        for line in lines:
            if line.startswith("user:"):
                st.session_state.messages.append({"role": "user", "content": line.replace("user: ", "")})
            if line.startswith("assistant:"):
                st.session_state.messages.append({"role": "assistant", "content": line.replace("assistant: ", "")})

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        # st.chat_message("user").write(prompt)  

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if check_button:
        results = quality_check_chatbot_used.bedrock_streaming_chat(dialogue_checker_used, st.session_state.messages)
        st.write(results)    
############### Logic ###############