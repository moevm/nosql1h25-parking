from django.contrib import admin
from .models import Parking
from .filters import (
    ParkingZoneFilter, AddressFilter, MinLatitudeFilter,
    MaxLatitudeFilter, MinLongitudeFilter, MaxLongitudeFilter,
    MinAvailableLotsFilter, MaxAvailableLotsFilter,
    MaxTotalLotsFilter, MinTotalLotsFilter,
    MinPricePerHourFilter, MaxPricePerHourFilter
)
from .forms import ParkingFilterForm
from pay_parking.filters import FakeFilterWithForm
from pay_parking.change_list import CustomChangeList
from django.urls import reverse
from django.utils.safestring import mark_safe


class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        'parking_zone',
        'address',
        'latitude',
        'longitude',
        'total_lots',
        'price_per_hour',
        'available_lots',
        'payments_link'
    )
    search_fields = ('address',)
    list_filter = (
        FakeFilterWithForm, ParkingZoneFilter, AddressFilter,
        MinLatitudeFilter, MaxLatitudeFilter,
        MinLongitudeFilter, MaxLongitudeFilter,
        MinAvailableLotsFilter, MaxAvailableLotsFilter,
        MaxTotalLotsFilter, MinTotalLotsFilter,
        MinPricePerHourFilter, MaxPricePerHourFilter
    )
    list_display_links = ('address',)
    list_editable = ('parking_zone', )

    def get_changelist(self, request, **kwargs):
        change_list_class = CustomChangeList
        change_list_class.filter_form_class = ParkingFilterForm
        return change_list_class

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('available_lots', 'payments_link')
        else:
            return ()
    
    @admin.display(description='Оплаты')
    def payments_link(self, parking):
        url = reverse("admin:paying_payment_changelist")
        url += f'?parking_id={parking.id}'
        link = f'<a href="{url}">Ссылка</a>'
        return mark_safe(link)

    show_facets = admin.ShowFacets.NEVER
    list_per_page = 10


admin.site.register(Parking, ParkingAdmin)
