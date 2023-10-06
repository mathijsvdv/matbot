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

ollama_run_mistral:
	ollama run mistral

.PHONY: init update install_ollama ollama_serve ollama_run_mistral
