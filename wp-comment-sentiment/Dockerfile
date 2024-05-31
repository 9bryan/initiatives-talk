# syntax=docker/dockerfile:1
FROM python:3.11.6-bullseye
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install cmake gcc musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY build.py .
RUN python build.py
COPY app.py .
CMD ["python", "-u", "app.py"]
