from django.contrib import admin
from django.urls import path
from .import_data import import_data
from .export_data import export_data
from django.http import HttpResponse
import json
from .forms import ImportForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest


class AdminSite(admin.AdminSite):
    def get_urls(self):
        new_urls = [
            path('import/', self.admin_view(self.import_view), name='import'),
            path('export/', self.admin_view(self.export_view), name='export')
        ]
        return new_urls + super().get_urls()

    def import_view(self, request):
        if request.method == 'POST':
            form = ImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    data = json.load(form.cleaned_data['import_file'])
                    try:
                        import_data(data)
                        messages.success(request, 'Данные загружены и обновлены')
                    except Exception as e:
                        messages.error(request, e)
                except Exception as e:
                    messages.error(request, "Ошибка при чтении файла")
                return redirect('admin:index')
        return HttpResponseBadRequest()
    
    def export_view(self, request):
        if request.method == 'GET':
            data = export_data()
            content = json.dumps(data, ensure_ascii=False)
            response = HttpResponse(content, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="export_data.json"'
            return response
        return HttpResponseBadRequest()


admin.site = AdminSite('')
