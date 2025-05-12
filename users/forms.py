import re

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator

from users.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    phone = forms.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^(\+7|8|7)\d{10}$',
                message="Телефон должен быть в формате: +79991234567 или 89991234567"
            )
        ],
        label='Телефон',
        help_text='Формат: +79991234567 или 89991234567',
        widget=forms.TextInput(attrs={
            'pattern': '^(\+7|8|7)\d{10,15}$',
            'title': 'Только цифры и символ + в начале',
            'maxlength': '18'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=True,
        label='Адрес доставки'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'password1',
            'password2'
        ]

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        # Удаляем все символы, кроме цифр и плюса
        cleaned_phone = re.sub(r'[^\d+]', '', phone)

        # Проверяем наличие +7 или 8 в начале
        if not re.match(r'^(\+7|8|7)', cleaned_phone):
            raise forms.ValidationError("Номер должен начинаться с +7, 7 или 8")

        # Нормализация номера
        if cleaned_phone.startswith('8'):
            cleaned_phone = '+7' + cleaned_phone[1:]
        elif cleaned_phone.startswith('7'):
            cleaned_phone = '+7' + cleaned_phone[1:]

        # Проверка длины
        if len(cleaned_phone) != 12:
            raise forms.ValidationError("Номер должен содержать ровно 11 цифр")

        # Проверка на повторяющиеся цифры
        if re.match(r'^(\+7|7|8)(\d)\2{9}$', cleaned_phone):
            raise forms.ValidationError("Номер не может состоять из повторяющихся цифр")

        return cleaned_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile = user.profile
            profile.phone = self.cleaned_data['phone']
            profile.address = self.cleaned_data['address']
            profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Электронная почта", required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # при желании можно добавить имя/фамилию

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {
            'address': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]
