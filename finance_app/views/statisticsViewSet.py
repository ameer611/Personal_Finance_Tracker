import io

import matplotlib.pyplot as plt
from django.db import models
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.views import APIView


from finance_app.models import Transaction


def get_user_income_expense_data(user):
    transactions = Transaction.objects.filter(user=user)
    income = transactions.filter(transaction_type=Transaction.INCOME).aggregate(total_income=models.Sum('amount'))['total_income'] or 0
    expense = transactions.filter(transaction_type=Transaction.EXPENSE).aggregate(total_expense=models.Sum('amount'))['total_expense'] or 0

    data = {
        'Income': income,
        'Expense': expense
    }
    return data

def get_user_category_income_data(user, data_type):
    transactions = Transaction.objects.filter(user=user, transaction_type=Transaction.data_type)
    data = {}
    for transaction in transactions:
        if transaction.category in data:
            data[transaction.category] += transaction.amount
        else:
            data[transaction.category] = transaction.amount

    return data


def generate_statistics_image(data):
    plt.figure(figsize=(10, 5))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    plt.title('User Data Statistics')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer


class UserStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        data = get_user_income_expense_data(user)

        buffer = generate_statistics_image(data)

        response = HttpResponse(buffer, content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="user_statistics.png"'
        return response


