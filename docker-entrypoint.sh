#!/bin/bash

ollama serve &

# Wait for server to start
until ollama list
do
    sleep 1
done

ollama pull mistral
ollama list

uvicorn fastapi_app:app --host 0.0.0.0 --port 5000
