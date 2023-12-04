from django.conf import settings
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from orders.exceptions import ItemNotExist, StripeIOException
from orders.models import Item
from orders.services import get_session_by_item_id, get_session_by_order_id


class BuyView(APIView):

    def get(self, request, item_id):
        try:
            session_id = get_session_by_item_id(item_id)
            return Response({'id': session_id})
        except StripeIOException as e:
            return Response(e.args, status=status.HTTP_424_FAILED_DEPENDENCY)
        except ItemNotExist as e:
            return Response(e.args, status=status.HTTP_404_NOT_FOUND)


class ItemView(APIView):

    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, item_id):
        data = dict()
        data['pk_test'] = settings.STRIPE.public_key
        if Item.objects.filter(pk=item_id).exists():
            data['item'] = Item.objects.get(pk=item_id)
        return Response(data, template_name='index.html')


class OrderView(APIView):

    def get(self, request, order_id):
        try:
            session_id = get_session_by_order_id(order_id)
            return Response({'id': session_id})
        except StripeIOException as e:
            return Response(e.args, status=status.HTTP_424_FAILED_DEPENDENCY)
        except ItemNotExist as e:
            return Response(e.args, status=status.HTTP_404_NOT_FOUND)
