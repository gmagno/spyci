"""Console script for spyci."""
import argparse
import textwrap
import sys

from spyci import spyci


def parse_args():
    description = textwrap.dedent("""
        Spyci (spyci v1.0.2) -- parses ngspice raw data files and
        plots the specified variables.
        For full documentation check the repo: https://github.com/gmagno/spyci
    """)

    epilog = r"""
                                                 /##
                                                |__/
          /#######  /######  /##   /##  /####### /##
         /##_____/ /##__  ##| ##  | ## /##_____/| ##
        |  ###### | ##  \ ##| ##  | ##| ##      | ##
         \____  ##| ##  | ##| ##  | ##| ##      | ##
         /#######/| #######/|  #######|  #######| ##
        |_______/ | ##____/  \____  ## \_______/|__/
                  | ##       /##  | ##              
                  | ##      |  ######/              
                  |__/       \______/               
    """

    epilog += textwrap.dedent("""
        return:
            The return value of %(prog)s is 0 if the raw file is successfully
            parsed and plotted.

        examples:
            # Run without arguments will attempt to load rawspice.raw from cwd
            # and plot all variables
            $ %(prog)s

            # List variables that can be plotted
            $ %(prog)s -l
            Variables:

            idx  name        type
            -----  ----------  -------
                1  i(l1)       current
                2  n1          voltage
                3  vi          voltage
                4  vo          voltage
                5  i(vsource)  current

            # Load 'some/location/sim.raw' and plot variables 'i(l1)' and 'vo'
            $ %(prog)s -r some/location/sim.raw "i(l1)" vo

            # Indices can be used insted of variable names, this is equivalent
            # to the previous example
            $ %(prog)s -r some/location/sim.raw 1 4

            # Save your plot to the file system
            $ %(prog)s -o myplot.png 1 4

            # Different image formats are supported, just use the correct
            # extension, {.png, .svg, .pdf, ...}. For a list of supported
            # formats run with -f flag
            $ %(prog)s -f
            Supported output image file formats:

            ext    format
            -----  -------------------------
            raw    Raw RGBA bitmap
            rgba   Raw RGBA bitmap
            pgf    PGF code for LaTeX
            svgz   Scalable Vector Graphics
            svg    Scalable Vector Graphics
            ps     Postscript
            png    Portable Network Graphics
            eps    Encapsulated Postscript
            pdf    Portable Document Format

        copyright:
            Copyright © 2020 Gonçalo Magno <goncalo@gmagno.dev>
            This software is licensed under the MIT License.
    """)
    parser = argparse.ArgumentParser(
        prog="spyci",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog)
    parser.add_argument("-v",
                        "--version",
                        required=False,
                        action='store_true',
                        help="shows %(prog)s version")
    parser.add_argument("-r",
                        "--raw-file",
                        required=False,
                        default="rawspice.raw",
                        action='store',
                        help="path to raw file to be parsed")
    parser.add_argument("-l",
                        "--list-variables",
                        required=False,
                        action='store_true',
                        help="lists variables that can be plotted")
    parser.add_argument("-f",
                        "--out-formats",
                        required=False,
                        action='store_true',
                        help="lists supported output image formats")
    parser.add_argument("-o",
                        "--out-image",
                        required=False,
                        action='store',
                        help="path to output image file, use -f, to list "
                        "supported formats")
    parser.add_argument("vars",
                        metavar='VARS',
                        nargs=argparse.REMAINDER,
                        help="List of variables to plot")
    args = vars(parser.parse_args())
    return args


def main():
    kwargs = parse_args()
    if kwargs['version']:
        print("Spice Raw Parse -- spyci v1.0.2")
        return 0

    if kwargs['list_variables']:
        try:
            spyci.list_vars(kwargs['raw_file'])
        except FileNotFoundError as e:
            print("Error: {}: {}".format(e.strerror, e.filename))
            return -1
        return 0

    if kwargs['out_formats']:
        try:
            spyci.img_formats()
        except FileNotFoundError as e:
            print("Error: {}: {}".format(e.strerror, e.filename))
            return -1
        return 0

    try:
        spyci.plot(kwargs['raw_file'], kwargs['vars'], kwargs['out_image'])
    except FileNotFoundError as e:
        print("Error: {}: {}".format(e.strerror, e.filename))
        return -1
    except spyci.InvalidVarsError:
        print("Error: Could not find variables: {}. For a list of valid "
              "variables run with '-l' flag".format(kwargs['vars']))
        return -1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
