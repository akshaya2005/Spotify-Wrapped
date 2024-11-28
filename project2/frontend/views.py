from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from .credentials import *


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

        # Check if the checkbox was checked
        has_spotify_account = request.POST.get('has_spotify_account')

        if form.is_valid():
            if not has_spotify_account:
                # Add error if the checkbox is not checked
                form.add_error('has_spotify_account', 'You must have a Spotify account to register.')
            else:
                # Save the new user if the form is valid and checkbox is checked
                form.save()
                return redirect('frontend:login')  # Redirect to login page after successful registration
        else:
            # If the form is invalid, add a general error message
            messages.error(request, 'Please correct the errors below.')

        return render(request, 'frontend/register.html', {'form': form})

    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})
# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         # Check if the checkbox was checked
#         has_spotify_account = request.POST.get('has_spotify_account')
#
#         if form.is_valid():
#             if not has_spotify_account:
#                 # Add error if the checkbox is not checked
#                 form.add_error('has_spotify_account', 'You must have a Spotify account to register.')
#             else:
#                 # Save the new user if the form is valid and checkbox is checked
#                 user = form.save()
#
#                 # Now, redirect the user to the Spotify authorization URL
#                 spotify_auth_url = get_spotify_auth_url(request, user)
#
#                 # Redirect to Spotify authentication page
#                 return redirect(spotify_auth_url)
#         else:
#             # If the form is invalid, add a general error message
#             messages.error(request, 'Please correct the errors below.')
#
#         return render(request, 'frontend/register.html', {'form': form})
#
#     else:
#         form = UserCreationForm()
#     return render(request, 'frontend/register.html', {'form': form})


def get_spotify_auth_url(request, user):
    """ Generate Spotify Auth URL to link account after registration """
    scope = 'user-read-private user-read-email'  # Define the scope you need from Spotify API
    redirect_uri = SPOTIPY_REDIRECT_URI
    client_id = SPOTIPY_CLIENT_ID
    client_secret = SPOTIPY_CLIENT_SECRET

    # Build the authorization URL
    auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'
    return auth_url


# Login view
def login_view(request):
    print("login_view called")
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("redirecting to index")
            # Redirect to index (Spotify connection page) after login
            return redirect('frontend:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})

# Logout view
def logout_view(request):
    # Log out of Django
    logout(request)

    # Render a template that logs out of Spotify and redirects to login
    return render(request, 'frontend/spotify_logout.html')