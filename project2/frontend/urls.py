from django.urls import path
from . import views

# Set the namespace for the application
app_name = 'frontend'

# Define URL patterns for the 'frontend' app
urlpatterns = [
    path('register/', views.register_view, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),  # Login URL
    path('logout/', views.logout_view, name='logout'),  # Logout URL
]
