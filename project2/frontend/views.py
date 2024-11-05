from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect



# Create your views here.

@login_required
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

@login_required
def intro_view(request):
    return render(request, 'frontend/intro.html')


# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('frontend:login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to index (Spotify connection page) after login
            return redirect('frontend:index')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('frontend:login')  # Redirect to login page after logout
