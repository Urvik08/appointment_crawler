FROM centos:centos7

RUN yum install -y initscripts

COPY . /home/visa_crawler

WORKDIR /home/visa_crawler

RUN python get-pip.py

RUN pip install selenium twilio

