from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_mongodb_backend.models import EmbeddedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class EmbeddedUser(EmbeddedModel):
    email = models.EmailField(verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    second_name = models.CharField(max_length=30, verbose_name='Фамилия')
    third_name = models.CharField(
        max_length=30, verbose_name='Отчество', null=True
    )
    created_at = models.DateField('Регистрация')
    is_staff = models.BooleanField(
        default=False, verbose_name='Статус персонала')

    def full_name(self):
        third_name = self.third_name if self.third_name is not None else ''
        return f'{self.first_name} {self.second_name} {third_name}'

    full_name.short_description = 'Фио пользователя'

    def __str__(self):
        third_name = self.third_name if self.third_name is not None else ''
        staff = '<br>Сотрудник' if self.is_staff is not None else ''
        return f'{self.first_name} {self.second_name} {third_name}' \
            f'<br>{self.email}' \
            f'{staff}'


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    second_name = models.CharField(max_length=30, verbose_name='Фамилия')
    third_name = models.CharField(
        max_length=30, verbose_name='Отчество', null=True, blank=True
    )
    objects = UserManager()
    is_staff = models.BooleanField(
        default=False, verbose_name='Статус персонала')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Последнее редактирование',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Регистрация',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    def __str__(self):
        third_name = self.third_name if self.third_name is not None else ''
        return f'{self.first_name} {self.second_name} {third_name}'

    def has_perm(self, *args, **kwargs):
        return self.is_staff

    def has_module_perms(self, *args, **kwargs):
        return self.is_staff

    def save(self, *args, **kwargs):
        if self.id:
            self.payments.update(
                user_detail=EmbeddedUser(
                    email=self.email,
                    first_name=self.first_name,
                    second_name=self.second_name,
                    third_name=self.third_name,
                    is_staff=self.is_staff,
                    created_at=self.created_at,
                )
            )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
