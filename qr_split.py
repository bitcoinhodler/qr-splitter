"""Read stdin, output HTML with QR codes."""

import argparse


def get_cmdline_args():
    """Parse cmdline and return Namespace."""
    parser = argparse.ArgumentParser(
        description="Multi QR code generator: reads data from stdin, "
        "writes HTML for printing to stdout.",
    )
    parser.add_argument('--title', help="title for page footer")
    parser.add_argument(
        '--version', type=int, default=16,
        help="QR code version to use (1-40, default %(default)s)",
    )
    return parser.parse_args()


def main():
    """Run main cmdline program."""
    args = get_cmdline_args()
    print(str(args))


if __name__ == "__main__":
    main()
