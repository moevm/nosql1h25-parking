from django.apps import AppConfig


class ParkingConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = 'parking'
    verbose_name = 'Парковки'