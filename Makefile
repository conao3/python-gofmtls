all:

.PHONY: format
format:
	pdm run ruff format
