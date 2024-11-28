from .models import Album, Author, Genre
from django.forms import EmailField, ValidationError, CharField, ModelForm, TextInput, Select, SelectMultiple, DateInput, Form, EmailInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'release_date', 'author', 'genres', 'users']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название альбома'
            }),
            'release_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата выхода альбома'
            }),
            'author': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Автор'
            }),
            'genres': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Жанры'
            }),
            'users': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Пользователи'
            })
        }

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя автора альбома'
            })
        }

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название жанра'
            })
        }

class UserForm(ModelForm):
    password = CharField(widget=PasswordInput, label='Пароль')
    confirm_password = CharField(widget=PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают.")

        return cleaned_data

class LoginForm(Form):
    username = CharField(label='Имя пользователя', max_length=100)
    password = CharField(widget=PasswordInput, label='Пароль')

from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email