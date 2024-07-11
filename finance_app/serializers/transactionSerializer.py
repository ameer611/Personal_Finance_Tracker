from datetime import datetime

from rest_framework import serializers

from finance_app.models import Transaction
from finance_app.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'description',
            'date',
            'created_at',
            'updated_at',
            'category',
            'transaction_type'
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0')
        return value

    def validate_date(self, value):
        if value < datetime(2015, 1, 1):
            raise serializers.ValidationError('Date must be after 2015-01-01')
        return value

    def validate_transaction_type(self, value):
        if value not in ['expense', 'income']:
            raise serializers.ValidationError('Transaction type must be either expense or income')
        return value

