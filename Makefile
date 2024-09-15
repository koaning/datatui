install:
	python -m pip install -e . twine wheel pytest ruff

pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

test:
	pytest

ruff:
	ruff check . --fix

check: ruff test

typerdocs: 
	typer datatui.app utils docs > docs/cli.md
