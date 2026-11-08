#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ -x .venv/bin/python ]; then
  .venv/bin/python -m streamlit run app.py --server.port 8511
else
  python3 -m streamlit run app.py --server.port 8511
fi
