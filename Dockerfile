FROM alpine
RUN apk update && \
 apk add --update haproxy \
 python \
 python-dev \
 py-pip \
 build-base \
 && pip install boto3

ADD hamba /usr/local/bin/hamba
ENV HOME /run
VOLUME /run
ENTRYPOINT ["hamba"]
