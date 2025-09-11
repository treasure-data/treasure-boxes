#!/usr/bin/env python3
"""
Standalone validation script for ID Unification YAML files.

This script can be run directly to validate unification YAML files without
needing to install the package.

Usage:
    python validate.py unification.yml
    python validate.py *.yml
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from cli import main

if __name__ == '__main__':
    main()