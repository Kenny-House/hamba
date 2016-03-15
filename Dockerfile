FROM alpine
RUN apk update && \
 apk add --update haproxy \
 python \
 python-dev \
 py-pip \
 build-base \
 && pip install boto3

ADD hamba /usr/local/bin/hamba
ADD fetch-keys.py /run/fetch-keys.py
ENV HOME /run
ENTRYPOINT ["hamba"]
