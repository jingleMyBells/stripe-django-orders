from django.conf import settings
import stripe
from requests.exceptions import RequestException

from orders.exceptions import ItemNotExist, OrderNotExist, StripeIOException
from orders.models import Item, Order

api_key = settings.STRIPE.secret_key
stripe.api_key = api_key


def create_product(name, description, tax_code=None):
    return stripe.Product.create(
        name=name,
        description=description,
        tax_code=tax_code,
    )


def create_price(product_id, unit_amount, currency):
    return stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
    )


def create_price_with_product_data(data, unit_amount, currency):
    return stripe.Price.create(
        product_data=data,
        unit_amount=unit_amount,
        currency=currency,
    )


def get_session(price_id):
    return stripe.checkout.Session.create(
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://example.com/success',
    )


def get_session_by_item_id(item_id: int):
    item = None

    if Item.objects.filter(pk=item_id).exists():
        item = Item.objects.get(pk=item_id)

    product_id = None
    price_id = None

    if item is None:
        raise ItemNotExist('Не удалось найти итем')

    if item.stripe_product_id and item.stripe_product_status == 'succeed':
        product_id = item.stripe_product_id

    if item.stripe_price_id and item.stripe_price_status == 'succeed':
        price_id = item.stripe_price_id

    if product_id is None:
        try:
            product_id = create_product(
                item.name,
                item.description,
                item.tax.stripe_id if item.tax is not None else None,
            ).id
        except RequestException:
            raise StripeIOException(
                'Ошибка взаимодействия с агрегатором платежей, '
                'повторите попытку позже',
            )
    if price_id is None:
        try:
            price_id = create_price(
                product_id,
                int(item.price * 100),
                item.currency,
            ).id
        except RequestException:
            raise StripeIOException(
                'Ошибка взаимодействия с агрегатором платежей, '
                'повторите попытку позже',
            )
    return get_session(price_id).id


def get_session_by_order_id(order_id):
    order = None

    if Order.objects.filter(pk=order_id).exists():
        order = Order.objects.get(pk=order_id)

    if order is None:
        raise OrderNotExist('Не удалось найти заказ')

    product_data = {
        'name': order.name,
        'tax_code': order.tax.stripe_id if order.tax is not None else None,
    }

    price = sum(order.items.all().values_list('price', flat=True))

    try:
        price_id = create_price_with_product_data(
            product_data,
            int(price * 100),
            settings.STRIPE.default_currency,
        ).id
        return get_session(price_id).id

    except RequestException:
        raise StripeIOException(
            'Ошибка взаимодействия с агрегатором платежей, '
            'повторите попытку позже',
        )
