from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi

from finance_app.views import TransactionViewSet, CategoryViewSet
from finance_app.views.statisticsViewSet import get_user_monthly_income_expense_data, \
    get_user_monthly_category_income_data, get_user_monthly_category_expense_data

schema_view = get_schema_view(
    openapi.Info(
        title="Finance Tracker Transactions",
        default_version='v1',
        description="API for track your incomes and outcomes",
        contact=openapi.Contact(email="oo1amirmuhammad@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)



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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]