from django import forms
from pay_parking.forms import FormWithFormsets, StatisticsForm
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Parking


class SearchParkingForm(forms.Form):
    parking_zone = forms.IntegerField(
        required=False, validators=[MinValueValidator(0)],
        label='Парковочная зона',
    )
    address = forms.CharField(required=False, label='Адрес')


class ParkingAdminForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = (
            'parking_zone', 'address', 'total_lots', 'latitude', 'longitude',
            'price_per_hour'
        )


class ParkingFilterForm(FormWithFormsets):
    parking_zone = forms.IntegerField(
        required=False, validators=[MinValueValidator(0)],
        label=''
    )
    address = forms.CharField(required=False, label='')
    min_latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        label='От',
    )
    max_latitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        label='До',
    )
    min_longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        label='От',
    )
    max_longitude = forms.DecimalField(
        max_digits=9, decimal_places=6,
        required=False,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        label='До',
    )
    min_total_lots = forms.IntegerField(
        required=False, label='От',
        validators=[MinValueValidator(0)]
    )
    max_total_lots = forms.IntegerField(
        required=False, label='До',
        validators=[MinValueValidator(0)]
    )
    min_available_lots = forms.IntegerField(
        required=False, label='От',
        validators=[MinValueValidator(0)]
    )
    max_available_lots = forms.IntegerField(
        required=False, label='До',
        validators=[MinValueValidator(0)]
    )
    min_price_per_hour = forms.DecimalField(
        max_digits=8, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        label='От',
    )
    max_price_per_hour = forms.DecimalField(
        max_digits=8, decimal_places=2,
        required=False,
        validators=[MinValueValidator(0)],
        label='До',
    )

    class Meta:
        fieldsets = (
            ('Зона парковки', {
                'fields': ('parking_zone', )
            }),
            ('Адрес', {
                'fields': ('address', )
            }),
            ('Широта', {
                'fields': ('min_latitude', 'max_latitude')
            }),
            ('Долгота', {
                'fields': ('min_longitude', 'max_longitude')
            }),
            ('Всего мест', {
                'fields': ('min_total_lots', 'max_total_lots')
            }),
            ('Свободные места', {
                'fields': ('min_available_lots', 'max_available_lots')
            }),
            ('Цена за час', {
                'fields': ('min_price_per_hour', 'max_price_per_hour')
            }),
        )


class ParkingStatisticsForm(StatisticsForm):
    y_choices = [
        ("total_lots", "Всего мест"),
        ("latitude", "Широта"),
        ("longitude", "Долгота"),
        ("price_per_hour", "Цена за час"),
        ("available_lots", "Свободные места"),
    ]
    x_choices = y_choices + [
        ("parking_zone", "Зона парковки"),
    ]
    x_attribute = forms.ChoiceField(choices=x_choices, label='Атрибут X', initial="parking_zone")
    y_attribute = forms.ChoiceField(choices=y_choices, label='Атрибут Y', initial="price_per_hour")