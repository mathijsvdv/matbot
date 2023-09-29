init:
	pre-commit install
	pre-commit autoupdate
	hatch env create
	hatch run python -m ipykernel install --user --name matbot --display-name "Python (matbot)"

update: init

.PHONY: init update
