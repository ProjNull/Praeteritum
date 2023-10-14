FROM python:3.11.4

WORKDIR /opt/prae-be/

COPY . .

RUN ["pip", "install", "-r", "./requirements.txt"]

EXPOSE 8002

CMD [ "python3", "main.py" ]

