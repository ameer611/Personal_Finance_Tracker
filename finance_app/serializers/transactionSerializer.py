import datetime

from rest_framework import serializers

from finance_app.models import Transaction, Category
from finance_app.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Transaction
        fields = (
            'id',
            'title',
            'amount',
            'description',
            'date',
            'created_at',
            'updated_at',
            'category',
            'transaction_type',
            'user'
        )
        read_only_fields = ['user']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0')
        return value

    def validate_date(self, value):
        if value < datetime.date(2015, 1, 1):
            raise serializers.ValidationError('Date must be after 2015-01-01')
        return value

    def validate_transaction_type(self, value):
        if value not in ['expense', 'income']:
            raise serializers.ValidationError('Transaction type must be either expense or income')
        return value

    def validate_category(self, value):
        user = self.context['request'].user
        if not Category.objects.filter(user=user, id=value.id).exists():
            raise serializers.ValidationError("Category does not exist")
        return value

