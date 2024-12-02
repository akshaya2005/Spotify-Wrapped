"""
ASGI config for project2.

This file sets up the ASGI application, which allows Django to handle
asynchronous protocols such as WebSockets in addition to HTTP.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project2.settings')

# Create the ASGI application callable
application = get_asgi_application()
