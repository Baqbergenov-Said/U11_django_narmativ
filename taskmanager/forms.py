from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

# Sing up from
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Parollarni solishtirish 
        if password != confirm_password:
            raise ValidationError("Parollar mos kelmadi!")
        return cleaned_data

# login into form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            # authenticate() chaqirish 
            user = authenticate(username=username, password=password)
            if user is None:
                # User topilmasa xatolik 
                raise ValidationError("Username yoki parol noto'g'ri!")
            cleaned_data['user'] = user
        return cleaned_data