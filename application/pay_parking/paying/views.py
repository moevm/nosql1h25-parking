from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import admin
from .models import Payment, Parking, now
from .forms import CreatePaymentForm, UserPaymentFilterForm, ConfirmCreatePaymentForm, datetime_format
from pay_parking.change_list import CustomChangeList
from django.contrib import messages
from django.urls import reverse
from .filters import (
    MinCreatedAtFiler, MaxCreatedAtFiler, MinStartFiler, MaxStartFiler,
    MinEndFiler, MaxEndFiler, MinPriceFiler, MaxPriceFiler,
    MinDurationFiler, MaxDurationFiler,
    AddressFiler, ParkingZoneFiler,
    MinLatitudeFilter, MaxLatitudeFilter, MaxLongitudeFilter,
    MinLongitudeFilter, MaxTotalLotsFilter, MinTotalLotsFilter,
    MaxPricePerHourFilter, MinPricePerHourFilter
)
from django.contrib.auth.decorators import login_required
from pay_parking.filters import FakeFilterWithForm
from pay_parking.admin import UserSite
from .admin import PaymentAdmin
from datetime import timedelta, datetime


class UserPaymentAdmin(PaymentAdmin):
    actions = None
    list_display = (
        'created_at',
        'start',
        'end',
        'price',
        'duration',
        'parking_address',
        'parking_zone',
    )
    list_display_links = None
    list_filter = (
        FakeFilterWithForm,
        MinCreatedAtFiler, MaxCreatedAtFiler, MinStartFiler, MaxStartFiler,
        MinEndFiler, MaxEndFiler, MinPriceFiler, MaxPriceFiler,
        MinDurationFiler, MaxDurationFiler,
        AddressFiler, ParkingZoneFiler,
        MinLatitudeFilter, MaxLatitudeFilter, MaxLongitudeFilter,
        MinLongitudeFilter, MaxTotalLotsFilter, MinTotalLotsFilter,
        MaxPricePerHourFilter, MinPricePerHourFilter
    )

    @admin.display(description='Адрес парковки', ordering='parking_detail__address')
    def parking_address(self, payment):
        return payment.parking_detail.address

    # parking_address.short_description = 'Адрес парковки'

    # parking_address.admin_order_field = 'parking_detail__address'


    def get_changelist(self, request, **kwargs):
        change_list_class = CustomChangeList
        change_list_class.filter_form_class = UserPaymentFilterForm
        return change_list_class

    def get_queryset(self, request):
        user = request.user
        queryset = Payment.objects.filter(user=user)
        return queryset

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_view_permission(self, *args, **kwargs):
        return True


user_site = UserSite('')
user_payment_admin = UserPaymentAdmin(Payment, user_site)


@login_required
def user_payments(request):
    response = user_payment_admin.changelist_view(request, extra_context={
        'title': 'Мои оплаты'
    })
    return response


@login_required
def create_payment(request, parking_id):
    parking = get_object_or_404(Parking, pk=parking_id)
    data = request.GET.copy()
    datetime_now = now()
    datetime_in_2_hours = datetime_now + timedelta(hours=2)
    data.update({
        'parking': parking,
    })
    if not data.get('start'):
        data['start'] = datetime_now
    if not data.get('end'):
        data['end'] = datetime_in_2_hours
    form = CreatePaymentForm(data)
    if {'start', 'end', } < set(request.GET) and form.is_valid():
        url = reverse("paying:confirm_create", args=[parking.id]) + '?'
        url += f'start={datetime.strftime(form.cleaned_data["start"], datetime_format)}'
        url += f'&end={datetime.strftime(form.cleaned_data["end"], datetime_format)}'
        return redirect(url)
    context = {
        'form': form,
        'parking': parking
    }
    return render(request, 'paying/create.html', context)


@login_required
def confirm_create(request, parking_id):
    parking = get_object_or_404(
        Parking,
        pk=parking_id
    )
    data = (request.POST or request.GET).copy()
    data.update({
        'parking': parking,
    })
    create_url = reverse("paying:create", args=[parking.id]) + '?'
    create_url += f'start={data["start"]}'
    create_url += f'&end={data["end"]}'
    form = ConfirmCreatePaymentForm(data)
    if not form.is_valid():
        for field_errors in form.errors.as_data().values():
            for error in field_errors:
                messages.error(request, error.message)
        return redirect(create_url)
    payment = form.save(commit=False)
    payment.user = request.user
    payment.parking = parking
    if request.method == 'POST':
        payment.save()
        messages.success(request, 'Оплата подтверждена')
        return redirect('paying:list')
    payment.duration = payment.calculate_duration()
    payment.price = payment.calculate_price()
    context = {
        'form': form,
        'payment': payment,
        'create_url': create_url
    }
    return render(request, 'paying/create_confirm.html', context)
