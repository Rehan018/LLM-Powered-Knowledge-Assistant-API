#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

EXPLANATION:
This file is the specific entry point for running commands in the terminal.
It reads the `DJANGO_SETTINGS_MODULE` environment variable to know which settings to use.

Common Commands used in this project:
1. `python manage.py runserver`: Starts the development web server.
2. `python manage.py makemigrations`: Detecting changes in `models.py`.
3. `python manage.py migrate`: Applying changes to the SQLite database.
4. `python manage.py ingest_kb`: Running our custom PDF ingestion command.
5. `python manage.py createsuperuser`: Creating an admin account.

Think of this as the "Remote Control" for your Django project.
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
