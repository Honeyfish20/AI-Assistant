#!/bin/bash

# 查找并杀死 Streamlit 进程
streamlit_pid=$(ps aux | grep "streamlit run" | grep -v grep | awk '{print $2}')
if [ -n "$streamlit_pid" ]; then
    echo "Killing Streamlit process with PID: $streamlit_pid"
    kill $streamlit_pid
fi

# 查找并杀死 Uvicorn 进程
uvicorn_pid=$(ps aux | grep "uvicorn" | grep -v grep | awk '{print $2}')
if [ -n "$uvicorn_pid" ]; then
    echo "Killing Uvicorn process with PID: $uvicorn_pid"
    kill $uvicorn_pid
fi