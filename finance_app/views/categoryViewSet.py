from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from finance_app.models import Category
from finance_app.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user).order_by('name')
        return queryset