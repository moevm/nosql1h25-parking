from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.main import ERROR_FLAG
from django.template.response import SimpleTemplateResponse
from django.contrib.admin.options import IncorrectLookupParameters
from django.http import HttpResponseRedirect


class UserSite(admin.AdminSite):
    enable_nav_sidebar = False

    def has_permission(self, request):
        return True


user_site = UserSite('')


class CustomModelAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    list_per_page = 10

    def get_urls(self):
        info = self.opts.app_label, self.opts.model_name
        new_urls = [
            path(
                'customisable_statistics/',
                self.admin_site.admin_view(self.customisable_statistics),
                name="%s_%s_customisable_statistics" % info
            ),
        ]
        return new_urls + super().get_urls()

    def customisable_statistics(self, request):
        try:
            cl = self.get_changelist_instance(request)
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET:
                return SimpleTemplateResponse(
                    "admin/invalid_setup.html",
                    {
                        "title": _("Database error"),
                    },
                )
            return HttpResponseRedirect(request.path + "?" + ERROR_FLAG + "=1")
        queryset = cl.queryset  # уже отфильтрованный
        
        context = dict(
            self.admin_site.each_context(request),
            cl=cl,
            title='Кастомизируемая статистика'
        )
        return render(request, "admin/customisable_statistics.html", context)
