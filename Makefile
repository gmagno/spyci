
.PHONY: all install test clean

all: clean install run-example-amplifier

build:
	python setup.py bdist_wheel
	python setup.py sdist

upload-dev:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	twine upload dist/*

install:
	python setup.py install

# test:
# 	py.test tests

run-example-amplifier:
	cd examples/amplifier && ngspice -r rawspice.raw -o output.log main.cir && python plot.py

clean:
	rm -rf dist/ build/ spr.egg*
