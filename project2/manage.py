#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script provides a command-line interface for managing your Django project.
It supports tasks like running the development server, applying migrations, and more.
"""
import os
import sys


def main():
    """
    The entry point for the Django management utility.

    Sets the default settings module and invokes Django's command-line execution
    for administrative tasks. Handles ImportError exceptions if Django isn't installed
    or properly configured.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')  # Set the default settings module
    try:
        from django.core.management import execute_from_command_line  # Import the execution utility
    except ImportError as exc:
        # Raise an error if Django is not installed or configured properly
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)  # Execute the command-line arguments


if __name__ == '__main__':
    main()  # Run the main function
