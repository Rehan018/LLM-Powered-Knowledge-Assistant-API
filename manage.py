#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This file is the specific entry point for running commands in the terminal.
It reads the environment settings and helps us manage the project.

We use this for everything from starting the web server to creating database tables 
and running our custom ingestion scripts. Think of this as the "Remote Control" 
for your Django project.
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
