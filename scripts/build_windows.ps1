$ErrorActionPreference = "Stop"

py -3 -m venv .venv-build
.\.venv-build\Scripts\python.exe -m pip install --upgrade pip
.\.venv-build\Scripts\python.exe -m pip install --upgrade ".[build]"
.\.venv-build\Scripts\python.exe -m PyInstaller `
  --name acell-acl `
  --onefile `
  --windowed `
  --clean `
  run.py

Write-Host "Windows build artifact: dist\acell-acl.exe"
