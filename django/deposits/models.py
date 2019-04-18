from django.db import models

from app.models import DefaultModel


class Deposit(DefaultModel):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'

    def __str__(self):
        return f'{self.country}, {self.city}'
