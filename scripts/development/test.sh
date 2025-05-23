#!/bin/bash

export ENV=test

python3 -m pytest --cov=saibyo tests/ -W ignore::DeprecationWarning --cov-report term-missing
