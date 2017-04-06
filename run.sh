#!/bin/bash
rm -r generated_output
rm -r app/static/js
mkdir app/static/js
mkdir generated_output
python3 main.py
