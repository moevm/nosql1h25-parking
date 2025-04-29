from django.contrib import admin


class UserSite(admin.AdminSite):
    enable_nav_sidebar = False

    def has_permission(self, request):
        return True


user_site = UserSite('')
