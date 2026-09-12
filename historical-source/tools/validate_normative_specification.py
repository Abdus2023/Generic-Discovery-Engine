#!/usr/bin/env python3
"""Validate the current normative specification protocol (v11.1).

The version-pinned implementation lives in validate_normative_specification_v111.py.
"""
import sys
from validate_normative_specification_v111 import main


if __name__ == "__main__":
    sys.exit(main())
