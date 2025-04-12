import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.contrib.auth import authenticate
from django.utils.timezone import now
from users.models import EmailVerification, User


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите пароль'})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user_cache = authenticate(self.request, email=email, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError("Неверный email или пароль")
                if not self.user_cache.is_active:
                    raise forms.ValidationError("Аккаунт неактивен")
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите фамилию'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'user-form__input', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'user-form__input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'user-form__input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'user-form__input', 'readonly': True}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'user-form__input', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'user-form__input', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
