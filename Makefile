PYTHON ?= python
PACKAGE_NAME ?= qa_framework

.PHONY: clean build-wheel check-wheel install-wheel smoke-wheel

clean:
	rm -rf build dist *.egg-info

build-wheel: clean
	$(PYTHON) -m pip install --upgrade pip build twine
	$(PYTHON) -m build

check-wheel:
	$(PYTHON) -m twine check dist/*

install-wheel:
	$(PYTHON) -m pip install --force-reinstall dist/$(PACKAGE_NAME)-*.whl

smoke-wheel:
	$(PYTHON) -c "from qa_framework import DataValidator, GreatExpectationsValidator; print('wheel import OK')"
