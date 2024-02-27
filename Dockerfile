FROM python:3.11.5-bookworm


ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y libpq-dev libpq5 mariadb-client 
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
ARG NODE_MAJOR=21
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt update
RUN apt install nodejs -y


COPY requirements* /geraipiapps/
COPY wait-for-mysql.sh /geraipiapps/

WORKDIR /geraipiapps

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x wait-for-mysql.sh
