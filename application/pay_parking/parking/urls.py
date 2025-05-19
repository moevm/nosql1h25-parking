from django.urls import path
from . import views

app_name = 'parking'
urlpatterns = [
    path('', views.index, name='list'),
]
