from django import forms
from .models import Payment, Parking, User
from django.core.validators import MinValueValidator, MaxValueValidator
from pay_parking.forms import FormWithFormsets, StatisticsForm
from .models import now
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone

datetime_format = '%Y-%m-%dT%H:%M'


class AdminPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('start', 'end', 'parking', 'user', )


def min_start(): return timezone.make_aware(
    datetime.now() - timedelta(minutes=5)
)


class CreatePaymentForm(forms.ModelForm):
    start = forms.DateTimeField(
        required=True, label='Начало ',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format=datetime_format),
        initial=lambda: now(),
        validators=[MinValueValidator(
            min_start,
            'Введите время не раньше текущего, чем на 5 минут'
        )],
    )
    end = forms.DateTimeField(
        required=True, label='Конец',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format=datetime_format),
        initial=lambda: now() + timedelta(hours=2)
    )
    parking = forms.ModelChoiceField(
        required=False,
        queryset=Parking.objects.all(),
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()
        if 'end' in cleaned_data and 'start' in cleaned_data:
            cleaned_data['end'].replace(second=0)
            cleaned_data['start'].replace(second=0)
            if (cleaned_data['end'] - cleaned_data['start']).total_seconds() / 3600 < 1:
                raise ValidationError(
                    'Укажите корректный промежуток времени от 1 часа')
            parking = cleaned_data['parking']
            available_lots = parking.total_lots - parking.payments.filter(
                start__lt=cleaned_data['end']
            ).filter(
                end__gt=self.cleaned_data['start']
            ).count()
            if available_lots <= 0:
                raise ValidationError(
                    'В указанный промежуток времени все парковочные места заняты')
        return cleaned_data

    class Meta:
        model = Payment
        fields = ('start', 'end', 'parking')


class ConfirmCreatePaymentForm(CreatePaymentForm):
    start = forms.DateTimeField(
        input_formats=[datetime_format],
        widget=forms.HiddenInput(),
        validators=[MinValueValidator(
            min_start,
            'Введите время не раньше текущего, чем на 5 минут'
        )],
    )
    end = forms.DateTimeField(
        input_formats=[datetime_format],
        widget=forms.HiddenInput()
    )
    parking = forms.ModelChoiceField(
        queryset=Parking.objects.all(),
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Payment
        fields = ('start', 'end', 'parking')


class UserPaymentFilterForm(FormWithFormsets):
    min_created_at = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_created_at = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    min_start = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_start = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    min_end = forms.DateTimeField(
        required=False, label='От',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    max_end = forms.DateTimeField(
        required=False, label='До',
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    min_price = forms.DecimalField(required=False, label='От',
                                   decimal_places=2, max_digits=8)
    max_price = forms.DecimalField(required=False, label='До',
                                   decimal_places=2, max_digits=8)
    min_duration = forms.FloatField(required=False, label='От')
    max_duration = forms.FloatField(required=False, label='До')
    address = forms.CharField(required=False, label='Адрес')
    parking_zone = forms.IntegerField(
        required=False, label='Номер парковочной зоны',
        validators=[MinValueValidator(0)],
    )
    min_total_lots = forms.IntegerField(
        validators=[MinValueValidator(0)],
        required=False,
        label='Мин. число мест'
    )
    max_total_lots = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(0)],
        label='Макс. число мест'
    )
    min_available_lots = forms.IntegerField(
        validators=[MinValueValidator(0)],
        required=False,
        label='Мин. число свободных мест'
    )
    max_available_lots = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(0)],
        label='Макс. число свободных мест'
    )
    min_price_per_hour = forms.DecimalField(
        max_digits=8, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        label='Мин. цена за час',
    )
    max_price_per_hour = forms.DecimalField(
        max_digits=8, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        label='Макс. цена за час',
    )
    min_longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        label='Мин. долгота',
    )
    max_longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        label='Макс. долгота',
    )
    min_latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        label='Мин. долгота',
    )
    max_latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        label='Макс. долгота',
    )

    class Meta:
        fieldsets = (
            ('Дата создания', {
                'fields': ('min_created_at', 'max_created_at')
            }),
            ('Дата начала', {
                'fields': ('min_start', 'max_start')
            }),
            ('Дата конца', {
                'fields': ('min_end', 'max_end')
            }),
            ('Цена', {
                'fields': ('min_price', 'max_price')
            }),
            ('Длительность (в часах)', {
                'fields': ('min_duration', 'max_duration')
            }),
            ('Парковка', {
                'fields': (
                    'address', 'parking_zone', 'min_total_lots', 'max_total_lots',
                    'min_available_lots', 'max_available_lots',
                    'min_price_per_hour', 'max_price_per_hour', 'min_longitude',
                    'max_longitude', 'min_latitude', 'max_latitude'
                )
            }),
        )


class PaymentFilterForm(UserPaymentFilterForm):
    first_name = forms.CharField(max_length=30, required=False, label='Имя')
    second_name = forms.CharField(
        max_length=30, required=False, label='Фамилия')
    third_name = forms.CharField(
        max_length=30, required=False, label='Отчество')
    email = forms.CharField(max_length=254, required=False, label='Email')
    is_staff = forms.BooleanField(required=False, label='Сотрудник')
    user_id = forms.ModelChoiceField(
        User.objects.all(),
        required=False, label='ID',
        widget=forms.TextInput()
    )
    parking_id = forms.ModelChoiceField(
        Parking.objects.all(),
        required=False, label='ID',
        widget=forms.TextInput()
    )

    class Meta:
        fieldsets = (
            ('Дата создания', {
                'fields': ('min_created_at', 'max_created_at')
            }),
            ('Дата начала', {
                'fields': ('min_start', 'max_start')
            }),
            ('Дата конца', {
                'fields': ('min_end', 'max_end')
            }),
            ('Цена', {
                'fields': ('min_price', 'max_price')
            }),
            ('Длительность (в часах)', {
                'fields': ('min_duration', 'max_duration')
            }),
            ('Парковка', {
                'fields': (
                    'address', 'parking_zone', 'min_total_lots', 'max_total_lots',
                    'min_price_per_hour', 'max_price_per_hour', 'min_longitude',
                    'max_longitude', 'min_latitude', 'max_latitude', 'parking_id'
                )
            }),
            ('Пользователь', {
                'fields': ('first_name', 'second_name', 'third_name', 'email', 'is_staff', 'user_id')
            }),
        )


class PaymentStatisticsForm(StatisticsForm):
    y_choices = [
        ("parking_detail__latitude", "Широта парковки"),
        ("parking_detail__latitude", "Долгота парковки"),
        ("parking_detail__total_lots", "Общее число мест парковки"),
        ("parking_detail__price_per_hour", "Цена за час парковки"),
        ("duration", "Длительность"),
        ("price", "Цена"),
    ]
    x_choices = y_choices + [
        ("parking_detail__parking_zone", "Номер парковочной зоны"),
        ("user_detail__is_staff", "Сотрудник"),
        ("created_at", "Создание"),
        ("start", "Начало"),
        ("end", "Конец"),
    ]
    x_attribute = forms.ChoiceField(choices=x_choices, label='Атрибут X', initial="parking_detail__parking_zone")
    y_attribute = forms.ChoiceField(choices=y_choices, label='Атрибут Y', initial="price")