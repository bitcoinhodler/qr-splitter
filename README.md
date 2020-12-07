# qr-splitter

This is a tool and Python library to take a (possibly large) block of
data and print that data onto one (or more) pages of QR codes.

It is useful to take e.g. a
[PSBT](https://bitcoinops.org/en/topics/psbt/) and print it for
offline signing by a
[HodlerGlacier](https://github.com/bitcoinhodler/GlacierProtocol)
quarantined laptop.

# How do I use it?

You need at least Python 3.7.

Run `make` to build a python venv; `source venv/bin/activate` to set
your PATH.

```
./qr_split.py --title="PSBT" my.psbt > my.html
firefox my.html
```

Then Ctrl-P in Firefox to print!
