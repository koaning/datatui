install:
	python -m pip install -e . twine wheel

pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
