# pull official base image
FROM python:3.9.1

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install cython==0.29.21 
RUN pip install --upgrade cython
RUN pip install -r requirements.txt
RUN python3 -m dostoevsky download fasttext-social-network-model
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# copy project
COPY . /usr/src/app/
