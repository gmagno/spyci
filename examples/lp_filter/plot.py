#!/usr/bin/env python

import numpy as np
from spr import load_raw
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def main():
    data = load_raw("rawspice.raw")
    gain = np.abs(data["values"]["vout"])/np.abs(data["values"]["vin"])
    # find the cutoff frequency
    v_db = 10*np.log10(np.abs(data["values"]["vout"]))
    idx = (np.abs(v_db-(-3))).argmin()
    cutoff_freq = np.around(
        np.real(data["values"]["frequency"][idx]), decimals=2)
    cutoff_gain = 10*np.log10(np.abs(data["values"]["vout"][idx]))

    fig, ax = plt.subplots()
    plt.title("Example: 2nd order low pass filter with lm741")
    plt.ylabel("Gain (dB)")
    plt.xlabel("Freq. (Hz)")
    plt.xscale("log")
    plt.yscale("linear")
    # plot gain
    plt.plot(
        np.real(data["values"]["frequency"]),
        10*np.log10(gain),
        label="Gain (vout/vin)",
    )
    # plot cutoff freq
    plt.plot(
        cutoff_freq,
        cutoff_gain,
        "bo"
    )
    ax.annotate(
        "cutoff (%.1eHz, %sdB)" % (cutoff_freq, np.around(cutoff_gain)),
        xy=(cutoff_freq, cutoff_gain),
        xytext=(10, -5),
        arrowprops=dict(facecolor="black", width=.1,
                        headwidth=2, headlength=5, shrink=0.05),
    )
    plt.legend()
    plt.grid(True)
    fig.tight_layout()
    plt.savefig("plot.svg")
    plt.savefig("plot.png")
    plt.show()


if __name__ == "__main__":
    main()
