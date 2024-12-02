from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


def register_view(request):
    """
    Handles user registration.

    - If the request is POST:
        - Processes the registration form.
        - Checks if the "has_spotify_account" checkbox is checked.
        - Saves the new user if the form is valid and the checkbox is checked.
        - Adds error messages to the context if validation fails.
    - If the request is GET:
        - Renders the registration page with a blank form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the login page.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        errors = []  # List to hold error messages

        # Check if the checkbox was checked
        has_spotify_account = request.POST.get('has_spotify_account')

        if form.is_valid():
            if not has_spotify_account:
                # Add error if the checkbox is not checked
                errors.append('You must have a Spotify account to register.')
            else:
                # Save the new user if the form is valid and checkbox is checked
                form.save()
                messages.success(request, "Registration successful! Please log in.")
                return redirect('frontend:login')
        else:
            # Add form errors to the errors list
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field.capitalize()}: {error}")

        return render(request, 'frontend/register.html', {'form': form, 'errors': errors})

    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form, 'errors': []})


def login_view(request):
    """
    Handles user login.

    - If the request is POST:
        - Authenticates the user using the provided credentials.
        - Redirects to the dashboard on successful login.
        - Adds error messages to the context if validation fails.
    - If the request is GET:
        - Renders the login page with a blank form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or a redirect to the dashboard page.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        errors = []  # List to hold error messages

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('frontend:dashboard')
        else:
            # Add form errors to the errors list
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(error)

        return render(request, 'frontend/login.html', {'form': form, 'errors': errors})

    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form, 'errors': []})


def logout_view(request):
    """
    Handles user logout.

    - Logs the user out of Django.
    - Renders a template to log out of Spotify and redirects to the login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered Spotify logout template.
    """
    # Log out of Django
    logout(request)

    # Render a template that logs out of Spotify and redirects to login
    return render(request, 'frontend/spotify_logout.html')
