#! /bin/bash

this_dir=$(dirname "$0")
export PATH="$PATH":"$this_dir"/usr/bin

"$this_dir"/usr/bin/python -m spyci.cli "$@"
