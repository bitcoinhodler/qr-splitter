#!/usr/bin/env python3
"""Read stdin, output HTML with QR codes."""

import argparse
import sys

import pyqrcode


def max_size(content, version, ecc):
    """Return the max bytes per QR code for the given content and ECC level."""
    contenttype, _ = pyqrcode.QRCode._detect_content_type(  # noqa:pylint-protected-access
        None, content, None
    )
    modenum = pyqrcode.tables.modes[contenttype]
    return pyqrcode.tables.data_capacity[version][ecc][modenum]


def get_cmdline_args():
    """Parse cmdline and return Namespace."""
    parser = argparse.ArgumentParser(
        description="Multi QR code generator: reads data from file "
        "(or stdin), writes HTML for printing to stdout.",
    )
    parser.add_argument('--title', help="title for page footer")
    parser.add_argument(
        '--version', type=int, default=16,
        help="QR code version to use (1-40, default %(default)s)",
    )
    parser.add_argument(
        '--ecc', choices=['L', 'M', 'Q', 'H'],
        default='M',
        help="error correction level (default %(default)s)",
    )
    parser.add_argument('input', metavar='FILE', nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="input file (stdin if none)")
    return parser.parse_args()


def main():
    """Run main cmdline program."""
    args = get_cmdline_args()
    print(str(args))
    indata = args.input.read()
    # Newlines require binary encoding (right?)
    indata = indata.rstrip()
    print("Input is:", indata)
    maxsize = max_size(indata, args.version, args.ecc)
    print("Found max size per QR code of", maxsize)
    # We don't need to specify version= because pyqrcode will use the
    # smallest version possible given the size of indata. It's okay to
    # use a smaller version if the data (or the last chunk of data) is
    # small.
    qr = pyqrcode.create(indata, error=args.ecc)
    print(qr.terminal())


if __name__ == "__main__":
    main()
