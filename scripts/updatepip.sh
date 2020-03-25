#!/bin/bash

# clean old files 
rm -rf build/
rm -rf dist/

# build new ones and update
python setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*