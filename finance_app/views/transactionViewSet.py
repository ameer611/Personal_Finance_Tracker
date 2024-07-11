from rest_framework.viewsets import ModelViewSet

from finance_app.models import Transaction
from finance_app.serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.all()
        return queryset