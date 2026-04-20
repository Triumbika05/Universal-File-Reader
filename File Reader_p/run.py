"""
run.py  —  Entry point for Universal File Reader (no frontend)

Usage:
    python run.py <file_path>

Examples:
    python run.py raw/employee_data.csv
    python run.py raw/data.txt
    python run.py raw/data.xml
    python run.py raw/downloaded.pdf
"""

import sys
import os

# Ensure the project root is always on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from triggers.cli import main

if __name__ == "__main__":
    main()
    