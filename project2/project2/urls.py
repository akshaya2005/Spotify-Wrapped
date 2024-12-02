"""
URL configuration for the project2 application.

This module defines the URL patterns for the project, routing requests to the appropriate
views. It supports function-based views, class-based views, and includes URL configurations
from other apps.

For more information, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
    - Function views:
        1. Add an import: from my_app import views
        2. Add a URL: path('', views.home, name='home')
    - Class-based views:
        1. Add an import: from other_app.views import Home
        2. Add a URL: path('', Home.as_view(), name='home')
    - Including another URLconf:
        1. Import the `include` function: from django.urls import include, path
        2. Add a URL: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns  # Import i18n_patterns for internationalization

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Redirect the root URL to the frontend login page
    path('', lambda request: redirect('frontend:login'), name='root_redirect'),

    # Include URL patterns from the frontend app
    path('frontend/', include('frontend.urls')),

    # Include URL patterns from the Spotify app
    path('spotify/', include('spotify.urls')),

    # Include URL patterns from the wraps app with a namespace for easier reference
    path('wraps/', include('wraps.urls', namespace='wraps')),
]
