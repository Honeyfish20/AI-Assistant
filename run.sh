read -p "Please choose whether to run locally (127.0.0.1) or on the public network (0.0.0.0). Input 0 for 127.0.0.1; Input 1 for 0.0.0.0:" choice

if [ $choice -eq "0" ]; then
    nohup bash -c 'cd frontend; streamlit run front.py --server.port 8502' > frontend.log 2>&1 &
    nohup bash -c 'cd backend; uvicorn backend.asgi:application --host 127.0.0.1 --port 8501' > backend.log 2>&1 &
    echo "Running on http://127.0.0.1:8501, please see backend.log if you cannot access your web"
elif [ $choice -eq "1" ]; then
    nohup bash -c 'cd frontend; streamlit run front.py --server.port 8502' > frontend.log 2>&1 &
    nohup bash -c 'cd backend; uvicorn backend.asgi:application --host 0.0.0.0 --port 8501' > backend.log 2>&1 &
    echo "Running on http://your_public_IP:8501, please see backend.log if you cannot access your web"
else
    echo "Invalid input, please run the script again."
    exit 1
fi

