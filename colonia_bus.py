#!/usr/bin/env python3

"""
HormigasAIS Edu Lab
Launcher compatible con mosquito-control original.

Ejecuta:
python3 colonia_bus.py
"""

import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))

target = os.path.join(
    BASE,
    "agents",
    "colonia_bus.py"
)

runpy.run_path(target, run_name="__main__")
