#!/usr/bin/env python3
"""Read stdin, output HTML with QR codes."""

import argparse
import contextlib
import html
import io
import sys

import pyqrcode


class MultiQR:
    """Represent a series of QR codes made from one big chunk of content."""

    def __init__(self, content, version, ecc):
        """Create new object."""
        self.content = content
        self.ecc = ecc
        self.max_size = self._max_size(version)

    def _max_size(self, version):
        """Return the max bytes per QR code."""
        contenttype, _ = pyqrcode.QRCode._detect_content_type(  # noqa:pylint-protected-access
            None, self.content, None
        )
        modenum = pyqrcode.tables.modes[contenttype]
        return pyqrcode.tables.data_capacity[version][self.ecc][modenum]

    def __iter__(self):
        """Yield QRCode objects from pyqrcode."""
        content = self.content
        while len(content) > 0:
            chunk = content[:self.max_size]
            content = content[self.max_size:]
            # We don't need to specify version= because pyqrcode will
            # use the smallest version possible given the size of
            # chunk. It's okay to use a smaller version if the data
            # (or the last chunk of data) is small.
            yield pyqrcode.create(chunk, error=self.ecc)


def get_cmdline_args():
    """Parse cmdline and return Namespace."""
    parser = argparse.ArgumentParser(
        description="Multi QR code generator: reads data from file "
        "(or stdin), writes HTML for printing to stdout.",
    )
    parser.add_argument('--title', help="title for page footer")
    parser.add_argument(
        '--version', type=int, default=16, metavar='[1-40]',
        choices=range(1,41),
        help="QR code version to use (default %(default)s)",
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


def print_html_for(title, qrcodes):
    """Print HTML."""
    htitle = html.escape(title or "")
    print("<!DOCTYPE html>")
    print(f"<html><head><title>{htitle}</title></head><body>")
    for pagenum, qrcode in enumerate(qrcodes, 1):
        print('<p style="margin:auto;">')
        imgdata = qrcode.png_as_base64_str()
        print(f'<img alt="QR" src="data:image/png;base64,{imgdata}"')
        print('style="page-break-after:always; width=100%;"/>')
        print('</p>')
    print("</body></html>")


def html_for(title, qrcodes):
    """Return string with HTML."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        print_html_for(title, qrcodes)
    return output.getvalue()


def main():
    """Run main cmdline program."""
    args = get_cmdline_args()
    indata = args.input.read()
    # Newlines require binary encoding (right?)
    indata = indata.rstrip()
    mqr = MultiQR(indata, args.version, args.ecc)
    print(html_for(args.title, mqr))


if __name__ == "__main__":
    main()
