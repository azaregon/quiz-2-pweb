FROM python:3.13-slim

RUN mkdir /home/themain
COPY . /home/themain

WORKDIR /home/themain

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-m app.main"]