#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citydigits.settings")

    from citydigits.settings import VENV_LIB
    if VENV_LIB not in sys.path:
	    sys.path.append( VENV_LIB )
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
