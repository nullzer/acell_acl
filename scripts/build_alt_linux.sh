#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv-build
.venv-build/bin/python -m pip install --upgrade pip
.venv-build/bin/python -m pip install --upgrade ".[build]"
.venv-build/bin/python -m PyInstaller \
  --name acell-acl \
  --onefile \
  --windowed \
  --clean \
  run.py

echo "ALT Linux build artifact: dist/acell-acl"
