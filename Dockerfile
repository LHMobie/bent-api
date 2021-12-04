FROM python:3.8

RUN apt-get -y update && \
    apt-get -y upgrade

RUN useradd bent && \
    mkdir -p /home/bent/.ssh && \
    chown -R bent. /home/bent/

ADD ./requirements.txt /root

RUN pip3 install -r /root/requirements.txt

RUN apt-get -y install curl

ADD . /home/bent

RUN chown -R bent:bent /home/bent

USER bent

WORKDIR /home/bent

EXPOSE 8000

ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "-p", "4", "--enable-threads", "--wsgi-file", "api.py", "--callable", "__hug_wsgi__"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]
