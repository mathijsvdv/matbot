API_PORT = 5000
IMAGE = matbot
CONTAINER = matbot

init:
	pre-commit install
	pre-commit autoupdate
	hatch env create
	hatch run python -m ipykernel install --user --name matbot --display-name "Python (matbot)"

update: init

install_ollama:
	curl https://ollama.ai/install.sh | sh

ollama_serve:
	ollama serve

ollama_pull_mistral:
	ollama pull mistral

ollama_run_mistral:
	ollama run mistral

chainlit:
	chainlit run chainlit_app.py

fastapi:
	uvicorn fastapi_app:app --port $(API_PORT) --reload

docker_build:
	docker build -t $(IMAGE) .

docker_run:
	docker run -d --name $(CONTAINER) -p $(API_PORT):$(API_PORT) --env-file .env $(IMAGE)

docker_rm:
	docker rm -f $(CONTAINER)

.PHONY: init update install_ollama ollama_serve ollama_pull_mistral ollama_run_mistral run serve docker_build docker_run docker_rm
