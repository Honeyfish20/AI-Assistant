FROM python:3.8-slim-buster
# Install Git
RUN apt-get update && apt-get install -y git

COPY . /usr/app/src
WORKDIR /usr/app/src
RUN pip install streamlit tqdm boto3
EXPOSE 8501

CMD ["sh", "-c", "streamlit run --browser.serverAddress 0.0.0.0 --server.enableCORS False --server.enableXsrfProtection False /usr/app/src/front.py" ]