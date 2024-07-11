from django.urls import path, include
from rest_framework.routers import DefaultRouter

from finance_app.views import TransactionViewSet, CategoryViewSet

transaction_router = DefaultRouter()
transaction_router.register(r'transactions', TransactionViewSet, basename='transactions')

category_router = DefaultRouter()
category_router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('transactions/', include(transaction_router.urls)),
    path('categories/', include(category_router.urls)),
]