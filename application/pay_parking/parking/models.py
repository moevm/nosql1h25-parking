from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_mongodb_backend.models import EmbeddedModel


class AbstractParking(models.Model):
    parking_zone = models.PositiveIntegerField('Зона парковки')
    address = models.CharField('Адрес', max_length=50)
    total_lots = models.PositiveIntegerField('Всего мест')
    latitude = models.DecimalField(
        'Широта',  max_digits=9, decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        'Долгота',  max_digits=9, decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    price_per_hour = models.DecimalField(
        'Цена за час',  decimal_places=2, max_digits=8,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        abstract = True


class EmbeddedParking(EmbeddedModel, AbstractParking):
    def __str__(self):
        return f'{self.address} ' \
            f'<br> Места: {self.total_lots} ' \
            f'<br>{self.price_per_hour} руб./час'


class ParkingManager(models.Manager):
    def get_queryset(self):
        from paying.models import Payment

        return super().get_queryset().annotate(
            available_lots=models.F('total_lots') - models.functions.Coalesce(
                models.Subquery(
                    Payment.objects.filter(
                        parking=models.OuterRef('id')
                    ).filter(
                        start__lte=models.functions.Now()
                    ).filter(
                        end__gte=models.functions.Now()
                    ).annotate(
                        count=models.Count('id')
                    ).values('count')
                ), 0
            )
        )


class Parking(AbstractParking):
    objects = ParkingManager()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'парковка'
        verbose_name_plural = 'Парковки'

    def save(self, *args, **kwargs):
        if self.id:
            self.payments.update(
                parking_detail=EmbeddedParking(
                    parking_zone=self.parking_zone,
                    address=self.address,
                    latitude=self.latitude,
                    longitude=self.longitude,
                    total_lots=self.total_lots,
                    price_per_hour=self.price_per_hour,
                )
            )
        return super().save(*args, **kwargs)
