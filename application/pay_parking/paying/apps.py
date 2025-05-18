from django.apps import AppConfig


class PayingConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'paying'
    verbose_name = 'Оплаты'
