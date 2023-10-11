API_PORT = 5000

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

run:
	chainlit run app.py

serve:
	uvicorn serve:app --port $(API_PORT) --reload

.PHONY: init update install_ollama ollama_serve ollama_pull_mistral ollama_run_mistral
