FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python3 python3-pip python3-dev ca-certificates openssl wget

RUN mkdir -p ~/.postgresql && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
         --output-document ~/.postgresql/root.crt && \
    chmod 0600 ~/.postgresql/root.crt




COPY requirements.txt /app/

RUN pip3 install --upgrade pip -r  /app/requirements.txt --break-system-packages

COPY ["./app.py", "/app/"]
COPY ["./postgre/.", "/app/postgre"]
COPY ["./pages/.", "/app/pages"]
COPY ["./images/.", "/app/images"]
COPY ["./utils/.", "/app/utils"]



RUN ls 
WORKDIR /app

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
