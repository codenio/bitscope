[![PyPI version](https://badge.fury.io/py/bitscope.svg)](https://badge.fury.io/py/bitscope)

# bitscope

Bitscope is a comprehensive library for collection of data from Bitscope Micro. It is a python wrapper for bitlib package installed using bitscope-library_2.0.FE26B and python-bindings-2.0-DC01L

## Setup

- clone this repository using
    ```bash
    $ git clone git@github.com:codenio/bitscope.git
    ```
- install `bitlib` library from ./src directory
    ```bash
    $ cd bitscope/src/
    # install the bitscope-library_2.0 debian package
    $ sudo apt-get install bitscope-library_2.0.FE26B_amd64.deb
    # install bitlib using the python-binding script
    $ cd python-bindings-2.0-DC01L/
    
    $ sudo python setup-bitlib.py install
    
    # in case of errors try
    
    $ sudo BASECFLAGS="" OPT="" CFLAGS="-O3" python setup-bitlib.py install
    ```

    Note: the files, debian packages and steps to install were taking from [murgen-dev-kit](https://github.com/kelu124/murgen-dev-kit/tree/master/software). thanks to [K.Ghosh](https://github.com/kelu124)

- form the root directory, install the bitscope python package using the `./install.sh` script

- connect your bitscope to your pc and test the functionality using
the example file at `./examples/scope/scope_plot.py`


## Contribute

You've discovered a bug or something else you want to change - excellent! - feel free to raise a issue.

You've worked out a way to fix it – even better! - submit your PR

You want to tell us about it – best of all!

Start contributing !