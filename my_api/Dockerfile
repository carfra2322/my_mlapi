# DATE: 12/02/2020
# NAME: Hector Carrillo
# DESCRIPTION: Docker file for the flask api

FROM python:3.6
# UPDATE
RUN apt-get update

# INSTALL REQUIREMENTS
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip3 install -r requirements.txt

# COPY APP
COPY . /
WORKDIR /

# RUN WSGI SERVER
CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "my_api.my_wsgi:app"]

