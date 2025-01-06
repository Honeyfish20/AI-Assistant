#!/bin/bash

conda create -n smart_training_assistant python=3.9 -y 
echo "Initializing conda for $(basename $SHELL)"
eval "$(conda shell.$(basename $SHELL) hook)"
conda activate smart_training_assistant
pip install streamlit tqdm boto3 django django-simpleui djangorestframework djangorestframework-simplejwt drf-yasg pymysql pycryptodomex aiohttp uvicorn