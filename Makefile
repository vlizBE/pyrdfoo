.PHONY: help check lint test docs clean

help:
	@echo 'Commands:'
	@echo '  make check    check types'
	@echo '  make lint     check coding rules'
	@echo '  make test     run tests'
	@echo '  make docs     generate the documentation'
	@echo '  make clean    clean up generated documentation files'

check:
	@poetry run pyright

lint:
	@poetry run ruff check

test:
	@poetry run python -m unittest test.rdfoo

docs:
	@poetry run sphinx-build -E -a -b html ./docs/source ./docs/build/html

clean:
	-rm -r ./docs/source/modules
	-rm -r ./docs/build
