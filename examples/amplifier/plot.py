#!/usr/bin/env python

import numpy as np
from spr import load_raw
import matplotlib.pyplot as plt

def main():
    data = load_raw("rawspice.raw")
    plt.figure()
    vars = ["vin", "vout",]
    plt.title("Example: inverting amplifier with lm741")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Time (s)")
    for v in vars:
        plt.plot(
            data["values"]["time"],
            data["values"][v],
            label=v,
        )
    plt.legend()
    plt.grid(True)
    plt.savefig("plot.svg")
    plt.savefig("plot.png")
    plt.show()

if __name__ == "__main__":
    main()
