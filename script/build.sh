#!/bin/bash

# get the git root directory
git_root=$(git rev-parse --show-toplevel)

cd $git_root

# clean the build artifacts
python setup.py clean

## create source distribution and wheel
# python setup.py sdist bdist_wheel
python setup.py bdist_wheel