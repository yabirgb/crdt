FROM python:alpine3.7

RUN apk update \
    && apk add build-base

RUN mkdir -p /app
COPY . /app
WORKDIR /app
EXPOSE 8000
RUN pip3 install -r requirements.txt
WORKDIR /app/src
CMD ["python", "main.py", "8000"]

