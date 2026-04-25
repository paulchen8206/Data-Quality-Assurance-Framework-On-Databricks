PACKAGE_NAME ?= qa_framework

.PHONY: clean build-wheel check-wheel install-wheel smoke-wheel

clean:
	rm -rf build dist *.egg-info

build-wheel: clean
	uv sync --all-groups
	uv build

check-wheel:
	uvx twine check dist/*

install-wheel:
	uv pip install --force-reinstall dist/$(PACKAGE_NAME)-*.whl

smoke-wheel:
	uv run python -c "from qa_framework import DataValidator, GreatExpectationsValidator; print('wheel import OK')"
