init:
	pre-commit install
	pre-commit autoupdate
	hatch env create

update: init

.PHONY: init update
