FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Install Ollama (mistral model)
RUN apt-get -y update; apt-get -y install curl
RUN curl https://ollama.ai/install.sh | sh

COPY ./src/ .
COPY *.py .
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
