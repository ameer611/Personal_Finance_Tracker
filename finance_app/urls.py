from django.urls import path, include
from rest_framework.routers import DefaultRouter

from finance_app.views import TransactionViewSet, CategoryViewSet
from finance_app.views.statisticsViewSet import get_user_monthly_income_expense_data, \
    get_user_monthly_category_income_data, get_user_monthly_category_expense_data



transaction_router = DefaultRouter()
transaction_router.register(r'transactions', TransactionViewSet, basename='transaction')

category_router = DefaultRouter()
category_router.register(r'categories', CategoryViewSet, basename='category')



urlpatterns = [
    path('transactions/', include(transaction_router.urls)),
    path('categories/', include(category_router.urls)),
    path('statistics/', get_user_monthly_income_expense_data, name='monthly-overall-statistics'),
    path('statistics/income/', get_user_monthly_category_income_data, name='monthly-income-statistics'),
    path('statistics/expense/', get_user_monthly_category_expense_data, name='monthly-expense-statistics'),
]