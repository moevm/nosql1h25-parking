from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_mongodb_backend.fields import EmbeddedModelField
from django.contrib.auth import get_user_model
from parking.models import Parking, EmbeddedParking
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import EmbeddedUser

User = get_user_model()


def min_start(): return timezone.make_aware(
    datetime.now() - timedelta(minutes=5)
)


def now(): return timezone.make_aware(datetime.now())



class Payment(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создание'
    )
    start = models.DateTimeField(
        'Начало', blank=False,
        # validators=[MinValueValidator(
        #     min_start,
        #     'Введите время не раньше текущего, чем на 5 минут'
        # )],
    )
    end = models.DateTimeField('Конец', blank=False)
    duration = models.DurationField('Длительность',)
    price = models.DecimalField(
        'Цена', decimal_places=2, max_digits=8
    )
    parking = models.ForeignKey(
        to=Parking, on_delete=models.SET_NULL, related_name='payments',
        verbose_name='Парковка', null=True)
    parking_detail = EmbeddedModelField(EmbeddedParking,
                                        verbose_name='Данные о парковке',
                                        )
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name='payments',
        verbose_name='Пользователь', null=True)
    user_detail = EmbeddedModelField(EmbeddedUser,
                                     verbose_name='Данные о пользователе',
                                     )

    def __str__(self):
        return f'{self.parking.address} {self.start-self.end}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'Оплаты'

    def save(self, *args, **kwargs):
        self.parking_detail = self.create_parking_detail()
        self.user_detail = self.create_user_detail()
        self.duration = self.calculate_duration()
        self.price = self.calculate_price()
        return super().save(*args, **kwargs)

    def create_parking_detail(self):
        return EmbeddedParking(
            parking_zone=self.parking.parking_zone,
            address=self.parking.address,
            latitude=self.parking.latitude,
            longitude=self.parking.longitude,
            total_lots=self.parking.total_lots,
            price_per_hour=self.parking.price_per_hour,
        )

    def create_user_detail(self):
        return EmbeddedUser(
            email=self.user.email,
            first_name=self.user.first_name,
            second_name=self.user.second_name,
            third_name=self.user.third_name,
            is_staff=self.user.is_staff,
            created_at=self.user.created_at,
        )

    def calculate_duration(self):
        return self.end - self.start
    
    def calculate_price(self):
        return round(
            self.duration.total_seconds() / 3600
            * float(self.parking.price_per_hour),
            2
        )

    # def clean(self):
    #     if self.start and self.end:
    #         self.end.replace(second=0)
    #         self.start.replace(second=0)
    #         if (self.end - self.start).total_seconds() / 3600 < 1:
    #             raise ValidationError(
    #                 'Укажите корректный промежуток времени от 1 часа')
    #         parking = self.parking
    #         available_lots = parking.total_lots - parking.payments.filter(
    #             start__lt=self.end
    #         ).filter(
    #             end__gt=self.start
    #         ).count()
    #         if available_lots == 0:
    #             raise ValidationError(
    #                 'В указанный промежуток времени все парковочные места заняты')

    #     return super().clean()
