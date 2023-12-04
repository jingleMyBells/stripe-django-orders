from requests.exceptions import RequestException

from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Item
from orders.services import create_product, create_price


@receiver(post_save, sender=Item, dispatch_uid='create_stripe_product')
def create_stripe_product_for_item(sender, instance, **kwargs):
    if kwargs.get('created'):
        try:
            product = create_product(
                instance.name,
                instance.description,
                instance.tax.stripe_id if instance.tax is not None else None,
            ).id
            price = create_price(
                product,
                int(instance.price * 100),
                instance.currency,
            )
            instance.stripe_product_id = product
            instance.stripe_product_status = 'succeed'
            instance.stripe_price_id = price.id
            instance.stripe_price_status = 'succeed'
            instance.save()
        except RequestException:
            instance.stripe_product_status = 'failed'
            instance.save()
