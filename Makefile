
.PHONY: all install test clean run-examples

all: clean install run-examples

build: clean
	python setup.py bdist_wheel
	python setup.py sdist

upload-dev:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: build
	twine upload dist/*

install:
	python setup.py install

# test:
# 	py.test tests

run-examples: run-example-amplifier run-example-lp_filter

run-example-amplifier:
	cd examples/amplifier && ngspice -r rawspice.raw -o output.log main.cir && python plot.py

run-example-lp_filter:
	cd examples/lp_filter && ngspice -r rawspice.raw -o output.log main.cir && python plot.py


clean:
	rm -rf dist/ build/ spr.egg*
