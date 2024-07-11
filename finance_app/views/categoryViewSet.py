from rest_framework.viewsets import ModelViewSet

from finance_app.models import Category
from finance_app.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by('name')
        return queryset