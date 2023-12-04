from django.contrib import admin

from orders.models import Currency, Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = (
        'stripe_product_status',
        'stripe_price_status',
    )
    list_display = (
        'name',
        'price',
        'currency',
        'stripe_product_status',
        'stripe_price_status',
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
