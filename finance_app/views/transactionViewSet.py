from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from finance_app.models import Transaction
from finance_app.serializers import TransactionSerializer, CategorySerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def category(self, request, *args, **kwargs):
        transaction = self.get_object()
        serializer = CategorySerializer(transaction.category)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def income(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        income_transactions = queryset.filter(transaction_type=Transaction.INCOME)
        filtered_queryset = self.filter_queryset(income_transactions)
        serializer = TransactionSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

