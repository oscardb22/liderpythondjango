from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Municipio(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=255, unique=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)

    estado = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return f'[{self.codigo}] - {self.nombre}'

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'


class Region(models.Model):
    codigo = models.CharField(verbose_name='Codigo', max_length=255, unique=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=255)
    municipios = models.ManyToManyField(
        Municipio,
        verbose_name='Municipios',
        blank=True,
    )

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'

    def __str__(self):
        return f'[{self.codigo}] - {self.nombre}'


class Users(AbstractUser):
    pro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Responsable',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_full_name()}'
