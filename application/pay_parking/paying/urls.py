from django.urls import path
from . import views

app_name = 'paying'
urlpatterns = [
    path('list/', views.user_payments, name='list'),
    path('create/<slug:parking_id>/', views.create_payment, name='create'),
    path('create/<slug:parking_id>/confirm/', views.confirm_create, name='confirm_create'),
]