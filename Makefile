CLI_VERSION=$(shell grep '^__version__' src/globus_cli/version.py | cut -d '"' -f2)

.venv:
	virtualenv .venv
	.venv/bin/pip install -U pip setuptools
	.venv/bin/pip install -e '.[development]'

.PHONY: localdev
localdev: .venv


.PHONY: lint test reference
lint:
	tox -e lint,mypy
reference:
	tox -e reference
test:
	tox

.PHONY: showvars prepare-release release
showvars:
	@echo "CLI_VERSION=$(CLI_VERSION)"
prepare-release:
	tox -e prepare-release
	$(EDITOR) changelog.adoc
release:
	git tag -s "$(CLI_VERSION)" -m "v$(CLI_VERSION)"
	tox -e publish-release

.PHONY: clean
clean:
	rm -rf .venv .tox dist build *.egg-info
