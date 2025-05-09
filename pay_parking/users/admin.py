from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import UserFilterForm, UserAdminForm
from pay_parking.change_list import CustomChangeList
from pay_parking.filters import FakeFilterWithForm
from .filters import (
    FirstNameFiler, SecondNameFiler, ThirdNameFiler, EmailFiler,
    IsStaffFiler, MaxCreatedAtFiler, MinCreatedAtFiler,
    MaxUpdatedAtFiler, MinUpdatedAtFiler,
    MaxLastLoginFiler, MinLastLoginFiler
)


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        'email',
        'first_name',
        'second_name',
        'third_name',
        'is_staff',
        'last_login',
        'created_at',
        'updated_at',
        'payments_link'
    )
    search_fields = ('email', 'first_name', 'second_name', 'third_name')
    list_filter = (
        FakeFilterWithForm,
        FirstNameFiler, SecondNameFiler, ThirdNameFiler, EmailFiler,
        IsStaffFiler, MaxCreatedAtFiler, MinCreatedAtFiler,
        MaxUpdatedAtFiler, MinUpdatedAtFiler,
        MaxLastLoginFiler, MinLastLoginFiler
    )
    list_display_links = ('email', 'first_name', 'second_name')

    def payments_link(self, user):
        url = reverse("admin:paying_payment_changelist")
        url += f'?user_id={user.id}'
        link = f'<a href="{url}">Ссылка</a>'
        return mark_safe(link)

    payments_link.short_description = 'Оплаты'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('updated_at', 'last_login', 'password', 'payments_link')
        else:
            return ()
    
    def get_changelist(self, request, **kwargs):
        change_list_class = CustomChangeList
        change_list_class.filter_form_class = UserFilterForm
        return change_list_class

    show_facets = admin.ShowFacets.NEVER


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
