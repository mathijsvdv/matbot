FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./src/ .
COPY *.py .

# EXPOSE 5000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "5000"]
