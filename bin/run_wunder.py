#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import app  # src/app.py is now imported as a module

if __name__ == "__main__":
    app.start()