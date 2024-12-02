from django.urls import path
from .views import dashboard, delete_wrap

app_name = 'wraps'  # Namespacing for the 'wraps' app

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),  # Route to the dashboard view
    path('delete/<int:wrap_id>/', delete_wrap, name='delete_wrap'),  # Route to delete a specific wrap by ID
]
