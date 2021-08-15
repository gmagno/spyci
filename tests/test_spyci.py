#!/usr/bin/env python
"""Tests for `spyci` package."""

# import pytest
import contextlib
from spyci import spyci
import io
import numpy as np

def test_dummy():
    print("Dummy test")

def test_load_ngspice_variables():

    # Load the correct answer
    correct_result_file = "result_skywater_char_variables.txt"
    correct_result_var = open(correct_result_file,"r").read()

    # Re-direct print to variable for comparison
    print_output = io.StringIO()
    with contextlib.redirect_stdout(print_output):
        spyci.list_vars("skywater_char_vgs.raw")
        result_var = print_output.getvalue()

    # Check assertion
    assert(correct_result_var == result_var)

def test_load_ngspice_content():

    # Load the correct answer
    correct_result_file = "result_skywater_char_values.txt"
    correct_result_values = open(correct_result_file,"r").read().strip('\n')

    data = spyci.load_raw("skywater_char_vgs.raw")
    result = np.array2string(data['values'])

    # Check assertion
    assert(correct_result_values == result)

if __name__ == "__main__":
    test_load_ngspice_variables()
    test_load_ngspice_content()

