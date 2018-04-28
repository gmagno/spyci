#!/usr/bin/env python

import re
import copy
import numpy as np


def load_raw(filename):
    """
    Parses an ascii raw data file, generates and returns a dictionary with the
    following structure:
        {
            "title": <str>,
            "date:": <str>,
            "plotname:": <str>,
            "flags:": <str>,
            "no_vars:": <str>,
            "no_points:": <str>,
            "vars": [
                { "idx": <int>, "name": <str>, "type": <str> },
                { "idx": <int>, "name": <str>, "type": <str> }
                ...
                { "idx": <int>, "name": <str>, "type": <str> }
            ]
            "values": {
                "var1": <numpy.ndarray>,
                "var2": <numpy.ndarray>,
                ...
                "varN": <numpy.ndarray>
            }
        }

        Arguments:
            :filename: path to file with raw data.
        Returns
            dict with structure described above.
    """
    with open(filename) as f:
        data = f.read()
    ret = {}
    pattern = (
        r"^Date:\s*(?P<date>\w.*?\w)\s*"
        r"Plotname:\s*(?P<plotname>\w.*?\w)\s*"
        r"Flags:\s*(?P<flags>\w.*?\w)\s*"
        r"No\. Variables:\s*(?P<no_vars>\d+)\s*"
        r"No\. Points:\s*(?P<no_points>\d+)\s*"
        r"Variables:\s*$(?P<vars>.*)^"
        r"Values:(?P<values>.*)"
    )
    m = re.search(pattern, data, re.MULTILINE | re.DOTALL)
    ret = copy.deepcopy(m.groupdict())
    ret.pop("values")

    # vars
    vars = m.groupdict()["vars"]
    pattern = (
        r"\s*(?P<idx>\d+)\s+"
        r"(?P<name>\S+)\s+"
        r"(?P<type>.*)\s*"
    )
    m_vars = re.finditer(pattern, vars)
    ret["vars"] = []
    for i in m_vars:
        ret["vars"].append(i.groupdict())
    ret["vars"].sort(cmp=lambda x, y: int(x["idx"])-int(y["idx"]))

    # values
    values = m.groupdict()["values"]
    pattern = (
        r"^\s*(?P<idx>\d+)\s+"
        r"(?P<values>\S+(?:\n\s*\S+)*)$"
    )
    m_values = re.finditer(pattern, values, re.MULTILINE)
    values = []
    for i in m_values:
        e = i.groupdict()["values"].split()
        values.append(tuple(e))
    values = [tuple(complex(*map(float, val.split(","))) for val in tup) for tup in values]
    dtype = []
    for x in ret["vars"]:
        dtype.append((x["name"], np.complex_))
    values = np.array(values, dtype=dtype)
    ret["values"] = values
    return ret
