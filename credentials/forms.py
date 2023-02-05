from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.forms import EmailField


class RegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name")
        field_classes = {
            'username': UsernameField,
            'email': EmailField,
        }
