from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    """
    A form for creating a new user account.

    Inherits from:
        UserCreationForm: A Django form that handles user registration.

    Meta:
        model (User): The User model provided by Django's authentication framework.
        fields (tuple): Specifies the fields to include in the form -
                        'username', 'email', 'password1', and 'password2'.

    Attributes:
        username (CharField): Input field for the username.
        email (EmailField): Input field for the email address.
        password1 (CharField): Input field for the first password entry.
        password2 (CharField): Input field for password confirmation.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """
    A form for authenticating an existing user.

    Inherits from:
        AuthenticationForm: A Django form that handles user login.

    Attributes:
        username (CharField): Input field for the username.
                              Rendered with a TextInput widget.
        password (CharField): Input field for the password.
                              Rendered with a PasswordInput widget.
    """
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
