# Set up python venv

.PHONY: all
all: venv

venv:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install wheel
	venv/bin/pip install pypng==0.0.20 PyQRCode==1.2.1 tidypy
