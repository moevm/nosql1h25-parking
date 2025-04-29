from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import CustomUserCreationForm


admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('parking:list'),
        ),
        name='registration',
    ),
    path('user/', include('users.urls')),
    path('payments/', include('paying.urls')),
    
    path('', include('parking.urls')),
]
