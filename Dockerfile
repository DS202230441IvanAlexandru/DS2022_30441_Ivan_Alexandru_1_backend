FROM ubuntu:14.04 as builder

RUN apt-get update

RUN apt-get -y install redis-server

FROM python:3.9.13
ENV DockerHOME=/home/app/webapp  

RUN mkdir -p $DockerHOME  

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=UTC
ENV POSTGRES_DB=energy_platform
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

RUN pip install --upgrade pip  
 
COPY . $DockerHOME
RUN pip install -r ./requirements.txt
EXPOSE 8000

CMD python manage.py runserver