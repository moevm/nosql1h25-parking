from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.main import ERROR_FLAG
from django.template.response import SimpleTemplateResponse
from django.contrib.admin.options import IncorrectLookupParameters
from django.http import HttpResponseRedirect
from django.db import models
from .forms import StatisticsForm
import plotly.express as px
from django.http import HttpResponseBadRequest  

class UserSite(admin.AdminSite):
    enable_nav_sidebar = False

    def has_permission(self, request):
        return True


user_site = UserSite('')


class CustomModelAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.NEVER
    list_per_page = 10
    statistics_form_class = StatisticsForm
    has_customisable_statistics = True

    def get_urls(self):
        new_urls= []
        if self.has_customisable_statistics:
            info = self.opts.app_label, self.opts.model_name
            new_urls = [
                path(
                    'customisable_statistics/',
                    self.admin_site.admin_view(self.customisable_statistics),
                    name="%s_%s_customisable_statistics" % info
                ),
            ]
        return new_urls + super().get_urls()
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_customisable_statistics'] = self.has_customisable_statistics
        return super().changelist_view(request, extra_context)

    def customisable_statistics(self, request):
        if not self.has_customisable_statistics:
            return HttpResponseBadRequest('This model has no customisable statistics')
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
        queryset = cl.queryset
        chart = None
        form = self.statistics_form_class(request.GET or None)
        if form.is_valid():
            x_attribute = form.cleaned_data["x_attribute"]
            y_attribute = form.cleaned_data["y_attribute"]
            queryset = queryset.values(x_attribute).annotate(
                **{y_attribute: models.Avg(y_attribute)}
            ).order_by(x_attribute)
            for item in queryset:
                print(type(item[x_attribute]))
            x_list = [item[x_attribute] for item in queryset]
            y_list = [item[y_attribute] for item in queryset]
            dict_choices = dict(form.fields['x_attribute'].choices)
            fig = px.line(
                x=x_list, y=y_list,
                labels={
                    "x": dict_choices[x_attribute],
                    "y": dict_choices[y_attribute]
                },
                title=f'Среднее значение "{dict_choices[y_attribute]}" от "{dict_choices[x_attribute]}"'
            )
            fig.update_layout(title_x=0.5)

            chart = fig.to_html()

        context = dict(
            self.admin_site.each_context(request),
            cl=cl,
            title='Кастомизируемая статистика',
            form=form,
            chart=chart
        )
        return render(request, "admin/customisable_statistics.html", context)
