from django.contrib import admin
from datetime import timedelta


class FilterWithoutTemplate(admin.SimpleListFilter):
    template = 'admin/empty.html'
    title = ''
    value_class = str

    def lookups(self, request, model_admin):
        return ((), )

    def choices(self, changelist):
        return
        yield


class FakeFilterWithForm(admin.SimpleListFilter):
    template = 'admin/filter_with_form.html'
    parameter_name = ''
    title = ''

    def lookups(self, request, model_admin):
        return ((), )

    def choices(self, changelist):
        yield {
            'form': changelist.filter_form
        }

    def queryset(self, request, queryset):
        pass


class ContainFilter(FilterWithoutTemplate):
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            value = self.value_class(self.value())
            return queryset.filter(
                **{f'{self.field_name}__icontains': value}
            )
        else:
            return queryset


class ExactFilter(FilterWithoutTemplate):
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            value = self.value_class(self.value())
            return queryset.filter(
                **{f'{self.field_name}__exact': value}
            )
        else:
            return queryset


class BooleanExactFilter(ExactFilter):
    value_class = bool


class IntergerExactFilter(ExactFilter):
    value_class = int


class MinFilter(FilterWithoutTemplate):
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            value = self.value_class(self.value())
            return queryset.filter(
                **{f'{self.field_name}__gte': value}
            )
        else:
            return queryset


class MaxFilter(FilterWithoutTemplate):
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            value = self.value_class(self.value())
            return queryset.filter(
                **{f'{self.field_name}__lte': value}
            )
        else:
            return queryset


class MinHourDurationFilter(MaxFilter):
    @staticmethod
    def value_class(hours): return timedelta(hours=float(hours))


class MaxHourDurationFilter(MaxFilter):
    @staticmethod
    def value_class(hours): return timedelta(hours=float(hours))
