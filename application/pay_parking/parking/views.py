from .models import Parking
from .admin import ParkingAdmin
from django.contrib.auth.decorators import login_required
from pay_parking.admin import user_site
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib import admin

class UserParkingAdmin(ParkingAdmin):
    actions = None
    list_display_links = None
    change_list_template = 'parking/parking_list.html'
    list_display = (
        'parking_zone',
        'address',
        'latitude',
        'longitude',
        'total_lots',
        'price_per_hour',
        'available_lots',
        'choose_link'
    )

    @admin.display(description='')
    def choose_link(self, parking):
        url = reverse("paying:create", args=[parking.id])
        link = f'<a href="{url}">Выбрать</a>'
        return mark_safe(link)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, *args, **kwargs):
        return False
    
    def has_delete_permission(self, *args, **kwargs):
        return False
    
    def has_view_permission(self, *args, **kwargs):
        return True


user_parking_admin = UserParkingAdmin(Parking, user_site)


def index(request):
    response = user_parking_admin.changelist_view(request, extra_context={
        'title': 'Выберите парковку'
    })
    return response
