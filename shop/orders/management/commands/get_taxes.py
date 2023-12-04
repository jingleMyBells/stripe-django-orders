from django.core.management.base import BaseCommand
import stripe

from orders.models import Tax


class Command(BaseCommand):
    help = 'Получает все налоги от Stripe'

    def handle(self, *args, **options):
        self.stdout.write(
            'Попробуем достать из Stripe налоги',
        )
        if Tax.objects.count() == 0:
            try:
                taxes = []
                response = stripe.TaxCode.list()
                for obj in response.get('data'):
                    if obj.get('object') is None:
                        continue
                    if obj.get('object') != 'tax_code':
                        continue
                    taxes.append(Tax(
                        stripe_id=obj.get('id'),
                        name=obj.get('name'),
                        description=obj.get('description'),
                    ))
                Tax.objects.bulk_create(taxes)
                self.stdout.write(
                    'Налоги получены',
                )
            except Exception:
                self.stdout.write(
                    'Что-то пошло не так, налоги не удалось выгрузить',
                )
        else:
            self.stdout.write(
                'Похоже что налоги уже выгружались ранее',
            )
