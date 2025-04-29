from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from pay_parking.forms import FormWithFormsets

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        labels = {
            "email": "Электронная почта",
            "third_name": "Отчество (если есть)"
        }
        model = User
        fields = ('email', 'first_name', 'second_name',
                  'third_name', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'second_name', 'third_name')

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'second_name', 'third_name', 'password', 'is_staff')

class UserFilterForm(FormWithFormsets):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    second_name = forms.CharField(
        max_length=30, required=False, label='Фамилия')
    third_name = forms.CharField(
        max_length=30, required=False, label='Отчество')
    email = forms.CharField(max_length=254, required=False, label='')
    is_staff = forms.BooleanField(required=False, label='')
    min_created_at = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_created_at = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    min_updated_at = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_updated_at = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    min_last_login = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_last_login = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        fieldsets = (
            ('Фио', {
                'fields': ('first_name', 'second_name', 'third_name')
            }),
            ('Email', {
                'fields': ('email', )
            }),
            ('Сотрудник', {
                'fields': ('is_staff', )
            }),
            ('Регистрация', {
                'fields': ('min_created_at', 'max_created_at')
            }),
            ('Последнее редактирование', {
                'fields': ('min_updated_at', 'max_updated_at')
            }),
            ('Последний вход', {
                'fields': ('min_last_login', 'max_last_login')
            })
        )
