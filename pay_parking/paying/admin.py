from django.contrib import admin
from .models import Payment
from .forms import AdminPaymentForm, PaymentFilterForm
from pay_parking.change_list import CustomChangeList
from django.utils.safestring import mark_safe
from django.urls import reverse
from .filters import (
    MinCreatedAtFiler, MaxCreatedAtFiler, MinStartFiler, MaxStartFiler,
    MinEndFiler, MaxEndFiler, MinPriceFiler, MaxPriceFiler,
    MinDurationFiler, MaxDurationFiler,
    AddressFiler, ParkingZoneFiler,
    FirstNameFiler, SecondNameFiler, ThirdNameFiler,
    EmailFiler, IsStaffFiler, UserIdFiler, ParkingIdFiler,
    MinLatitudeFilter, MaxLatitudeFilter, MaxLongitudeFilter,
    MinLongitudeFilter, MaxTotalLotsFilter, MinTotalLotsFilter,
    MaxPricePerHourFilter, MinPricePerHourFilter
)
from pay_parking.filters import FakeFilterWithForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Parking

class PaymentAdmin(admin.ModelAdmin):
    # actions = None
    form = AdminPaymentForm
    list_display = (
        'created_at',
        'start',
        'end',
        'price',
        'duration',
        'parking_link',
        'parking_zone',
        'user_link',
        'user_email',
        'user_is_staff'
    )
    search_fields = (
        'user_detail__email', 'user_detail__first_name',
        'user_detail__second_name', 'user_detail__third_name',
        'parking_detail__address'
    )

    list_filter = (
        FakeFilterWithForm,
        MinCreatedAtFiler, MaxCreatedAtFiler, MinStartFiler, MaxStartFiler,
        MinEndFiler, MaxEndFiler, MinPriceFiler, MaxPriceFiler,
        MinDurationFiler, MaxDurationFiler,
        AddressFiler, ParkingZoneFiler,
        FirstNameFiler, SecondNameFiler, ThirdNameFiler,
        EmailFiler, IsStaffFiler, UserIdFiler, ParkingIdFiler,
        MinLatitudeFilter, MaxLatitudeFilter, MaxLongitudeFilter,
        MinLongitudeFilter, MaxTotalLotsFilter, MinTotalLotsFilter,
        MaxPricePerHourFilter, MinPricePerHourFilter
    )

    def user_link(self, payment):
        url = reverse("admin:users_user_change", args=[payment.user_id])
        link = f'<a href="{url}">{payment.user_detail.full_name()}</a>'
        return mark_safe(link)

    def user_full_name(self, payment):
        return payment.user_detail.full_name()

    def user_email(self, payment):
        return payment.user_detail.email

    def user_is_staff(self, payment):
        return payment.user_detail.is_staff

    def parking_link(self, payment):
        url = reverse("admin:parking_parking_change",
                      args=[payment.parking_id])
        link = f'<a href="{url}">{payment.parking_detail.address}</a>'
        return mark_safe(link)
    
    def parking_zone(self, payment):
        return payment.parking_detail.parking_zone

    def parking_total_lots(self, payment):
        return payment.parking_detail.parking_zone

    user_full_name.short_description = 'Фио пользователя'
    user_email.short_description = 'Email'
    user_is_staff.short_description = 'Сотрудник'
    user_link.short_description = 'Пользователь'
    parking_link.short_description = 'Парковка'
    parking_zone.short_description = 'Пар. зона'
    parking_total_lots.short_description = 'Места'

    parking_link.admin_order_field = 'parking_detail__address'
    user_email.admin_order_field = 'user_detail__email'
    user_is_staff.admin_order_field = 'user_detail__is_staff'
    user_link.admin_order_field = 'user_id'
    parking_zone.admin_order_field = 'parking_detail__parking_zone'

    user_is_staff.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('duration', 'price', 'parking_detail', 'user_full_name', 'user_email', 'user_is_staff')
        else:
            return ()

    show_facets = admin.ShowFacets.NEVER

    def get_changelist(self, request, **kwargs):
        change_list_class = CustomChangeList
        change_list_class.filter_form_class = PaymentFilterForm
        return change_list_class

    def changelist_view(self, request, extra_context=None):
        user_id = request.GET.get('user_id')
        extra_context = {}
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            extra_context.update({
                'title': f'Оплаты пользователя {user}'
            })
        parking_id = request.GET.get('parking_id')
        if parking_id:
            parking = get_object_or_404(Parking, pk=parking_id)
            extra_context.update({
                'subtitle': f'Оплаты парковки {parking}'
            })
        return super().changelist_view(request, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        return super().add_view(request, form_url, extra_context)
admin.site.register(Payment, PaymentAdmin)
