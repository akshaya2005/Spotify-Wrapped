"""
WSGI config for the project2 application.

This file contains the configuration for the Web Server Gateway Interface (WSGI),
which serves as the entry point for WSGI-compatible web servers to serve your Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')

# Create the WSGI application callable
application = get_wsgi_application()

# Alias for compatibility with some deployment tools
app = application
