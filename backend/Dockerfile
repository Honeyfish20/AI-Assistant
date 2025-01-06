FROM python:3.8-slim-buster
# Install Git
RUN apt-get update && apt-get install -y git

COPY . /usr/app/src
WORKDIR /usr/app/src
RUN pip install -r requirements.txt
RUN mkdir -p /root/.aws
# Input your AKSK
RUN cat /root/.aws/credentials
RUN python manage.py collectstatic --no-input
EXPOSE 8501

CMD ["sh", "-c", "uvicorn backend.asgi:application --host 0.0.0.0 --port 8501" ]