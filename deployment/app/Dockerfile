FROM alpine

ADD /app  /app

WORKDIR /app

RUN apk update
RUN apk add py3-pip
RUN pip install -r requirements.txt

CMD gunicorn --log-level debug api:app -b 0.0.0.0:8000
