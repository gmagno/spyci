"""Main module."""

import copy
import os
import pathlib
import re

import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate


class InvalidVarsError(Exception):
    pass


def load_raw(rawfile):
    """
    Parses an ascii raw data file and returns a dictionary with the following
    structure:
        {
            'title': <str>,
            'date:': <str>,
            'plotname:': <str>,
            'flags:': <str>,
            'no_vars:': <str>,
            'no_points:': <str>,
            'vars': [
                { 'idx': <int>, 'name': <str>, 'type': <str> },
                { 'idx': <int>, 'name': <str>, 'type': <str> }
                ...
                { 'idx': <int>, 'name': <str>, 'type': <str> }
            ]
            'values': {
                'var1': <numpy.ndarray>,
                'var2': <numpy.ndarray>,
                ...
                'varN': <numpy.ndarray>
            }
        }

    Arguments:
        :filename: path to file with raw data.
    Returns
        dict with structure described above.
    """

    path = os.path.realpath(rawfile)
    data = pathlib.Path(path).read_text()
    ret = {}
    pattern = (r"^Title:\s*(?P<title>.*)\s*"
               r"^Date:\s*(?P<date>\w.*?\w)\s*"
               r"Plotname:\s*(?P<plotname>\w.*?\w)\s*"
               r"Flags:\s*(?P<flags>\w.*?\w)\s*"
               r"No\. Variables:\s*(?P<no_vars>\d+)\s*"
               r"No\. Points:\s*(?P<no_points>\d+)\s*"
               r"Variables:\s*$(?P<vars>.*)^"
               r"Values:(?P<values>.*)")
    m = re.search(pattern, data, re.MULTILINE | re.DOTALL)
    ret = copy.deepcopy(m.groupdict())
    ret.pop('values')

    # vars
    vars = m.groupdict()['vars']
    pattern = (r"\s*(?P<idx>\d+)\s+" r"(?P<name>\S+)\s+" r"(?P<type>.*)\s*")
    m_vars = re.finditer(pattern, vars)
    ret['vars'] = []
    for i in m_vars:
        ret['vars'].append(i.groupdict())

    # values
    values = m.groupdict()['values']
    pattern = (r"^\s*(?P<idx>\d+)\s+" r"(?P<values>\S+(?:\n\s*\S+)*)$")
    m_values = re.finditer(pattern, values, re.MULTILINE)
    values = []
    for i in m_values:
        e = i.groupdict()['values'].split()
        values.append(tuple(e))
    values = [
        tuple(complex(*map(float, val.split(','))) for val in tup)
        for tup in values
    ]
    dtype = []
    for x in ret['vars']:
        dtype.append((x['name'], np.complex_))
    values = np.array(values, dtype=dtype)
    ret['values'] = values
    return ret


def list_vars(rawfile):
    """Loads the rawspice file and prints the variables to plot.
        Args
        rawfile: path to the rawspice.raw file
    """
    data = load_raw(rawfile)
    pvars = sorted(data['vars'], key=lambda v: v['idx'])
    pvars.pop(0)

    trows = [[v['idx'], v['name'], v['type']] for v in pvars]
    theader = ['idx', 'name', 'type']

    print("Variables:\n")
    print(tabulate(trows, headers=theader))


def img_formats():
    formats = plt.gcf().canvas.get_supported_filetypes()
    trows = [[k, v] for k, v in formats.items()]
    theader = ['ext', 'format']
    print("Supported output image file formats:\n")
    print(tabulate(trows, headers=theader))


def plot(rawfile, pvars=None, outimg=None):
    """Loads the rawspice file and plots the data.
        Args
        rawfile: path to the rawspice.raw file
        pvars: list of variables to plot. If `None`, all variables are
        plotted.
        save: path to save file
    """
    # FIXME: some poop logic here... should definitely fix this
    d = load_raw(rawfile)
    file_vars = sorted(d['vars'], key=lambda v: v['idx'])

    if pvars:
        pvars = [
            v for v in file_vars if v['name'] in pvars or v['idx'] in pvars
        ]
    else:
        pvars = file_vars
        pvars.pop(0)  # pop first variable, either 'time' or 'frequency'

    if not pvars:
        raise InvalidVarsError()

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    if d['plotname'] == "Transient Analysis":
        xx = d['values']['time']
        ax1.set_xscale('linear')
        ax1.set_yscale('linear')
        ax2.set_yscale('linear')
        ax1.set_xlabel("Time (s)")
    elif d['plotname'] == "AC Analysis":
        xx = d['values']['frequency']
        ax2.set_xscale('log')
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        ax1.set_xlabel("Frequency (Hz)")
    else:
        print("Error: unsupported plotname")
        return -1

    ax1.set_ylabel("Voltage (V)")
    ax2.set_ylabel("Current (A)")

    lines1 = []
    lines2 = []
    for i, v in enumerate(pvars):
        if v['type'] == 'voltage':
            ln1 = ax1.plot(xx.real,
                           d['values'][v['name']].real,
                           label=v['name'],
                           color=plt.cm.tab10(i))
            lines1.append(ln1)
        elif v['type'] == 'current':
            ln2 = ax2.plot(xx.real,
                           d['values'][v['name']].real,
                           label=v['name'],
                           color=plt.cm.tab10(i))
            lines2.append(ln2)

    ax1.tick_params(axis='x', colors='black')
    ax1.xaxis.label.set_color('black')
    if lines1:
        ax1.legend(loc='upper left')
        ax1.grid(True)
        ax1.tick_params(axis='y', colors='blue')
        ax1.yaxis.label.set_color('blue')
    else:
        ax1.tick_params(axis='y', colors='white')
        ax1.yaxis.label.set_color('white')
    if lines2:
        ax2.legend(loc='upper right')
        if not lines1:
            ax1.xaxis.grid(True)
            ax2.yaxis.grid(True)
        ax2.tick_params(axis='y', colors='red')
        ax2.yaxis.label.set_color('red')
    else:
        ax2.tick_params(axis='y', colors='white')
        ax2.yaxis.label.set_color('white')

    plt.title("{}\n{}, {}".format(d['title'], d['plotname'], d['date']),
              color='black')

    if outimg:
        plt.savefig(outimg, bbox_inches='tight')

    fig.tight_layout()
    plt.show()
