from django.conf import settings
from django.db import models


class Currency(models.Model):

    name = models.CharField(
        'наименование',
        max_length=10,
        choices=settings.STRIPE.currencies,
    )

    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'валюты'

    def __str__(self):
        return self.name


class Tax(models.Model):
    stripe_id = models.CharField(
        verbose_name='код налога',
        max_length=20,
        unique=True,
    )
    name = models.CharField(verbose_name='название', max_length=255)
    description = models.CharField(verbose_name='описание', max_length=1000)

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(verbose_name='название', max_length=255)
    description = models.CharField(verbose_name='описание', max_length=1000)
    price = models.FloatField(verbose_name='цена')
    currency = models.ForeignKey(
        Currency,
        verbose_name='валюта',
        on_delete=models.CASCADE,
    )
    stripe_product_id = models.CharField(
        verbose_name='внешний идентификатор продукта',
        max_length=100,
        null=True,
        editable=False,
    )
    stripe_price_id = models.CharField(
        verbose_name='внешний идентификатор цены',
        max_length=100,
        null=True,
        editable=False,
    )
    stripe_product_status = models.CharField(
        verbose_name='статус получения внешнего ID продукта',
        max_length=25,
        default='pending',
        editable=False,
    )
    stripe_price_status = models.CharField(
        verbose_name='статус получения внешнего ID цены',
        max_length=25,
        default='pending',
        editable=False,
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='налог',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(
        verbose_name='название заказа',
        max_length=255,
    )
    items = models.ManyToManyField(
        Item,
        verbose_name='товары в заказе',
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='налог',
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return self.name
