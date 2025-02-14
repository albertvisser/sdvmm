#! /usr/bin/env python
"""(Stardew Valley) Mods Manager: visual tool to activate and deactivate mods
"""
import sys
from src import manager

if len(sys.argv) > 1 and sys.argv[1] in ('-r', '--rebuild'):
    manager.main(rebuild=True)
else:
    manager.main()
