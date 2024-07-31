from rest_framework.decorators import api_view
from rest_framework.response import Response

from finance_app.models import Transaction


from django.db.models import Sum
from django.db.models.functions import TruncMonth

@api_view(['GET'])
def get_user_monthly_income_expense_data(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Aggregate income data by month
    monthly_income = transactions.filter(transaction_type=Transaction.INCOME).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total_income=Sum('amount')).order_by('month')

    # Aggregate expense data by month
    monthly_expense = transactions.filter(transaction_type=Transaction.EXPENSE).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(total_expense=Sum('amount')).order_by('month')

    # Prepare data in a dictionary format for easy access
    data = {
        'Income': list(monthly_income),
        'Expense': list(monthly_expense)
    }
    return Response(data)



@api_view(['GET'])
def get_user_monthly_category_income_data(request):
    # Filter transactions by user and type
    transactions = Transaction.objects.filter(user=request.user, transaction_type=Transaction.INCOME)

    # Aggregate data by month and category
    monthly_category_data = transactions.annotate(
        month=TruncMonth('date')
    ).values('month', 'category').annotate(total_amount=Sum('amount')).order_by('month', 'category')

    # Convert to a more convenient data structure
    data = {}
    for item in monthly_category_data:
        month = item['month'].strftime('%Y-%m')
        category = item['category']
        amount = item['total_amount']

        if month not in data:
            data[month] = {}

        data[month][category] = amount

    return Response(data)

@api_view(['GET'])
def get_user_monthly_category_expense_data(request):
    # Filter transactions by user and type
    transactions = Transaction.objects.filter(user=request.user, transaction_type=Transaction.EXPENSE)

    # Aggregate data by month and category
    monthly_category_data = transactions.annotate(
        month=TruncMonth('date')
    ).values('month', 'category').annotate(total_amount=Sum('amount')).order_by('month', 'category')

    # Convert to a more convenient data structure
    data = {}
    for item in monthly_category_data:
        month = item['month'].strftime('%Y-%m')
        category = item['category']
        amount = item['total_amount']

        if month not in data:
            data[month] = {}

        data[month][category] = amount

    return Response(data)





