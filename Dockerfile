# pull official base image
FROM --platform=linux/amd64 python:3.10

# set work directory
WORKDIR /GateApproval

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# copy project
COPY . .
RUN pip install --upgrade pip
# RUN pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.9.0-py3-none-any.whl
RUN pip install -e .

# install dependencies
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

EXPOSE 9060

RUN bash deploy.sh 9060