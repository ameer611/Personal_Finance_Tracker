from django.urls import path
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

from user_app.views import RegisterView, LoginView, LogoutView, UserView

schema_view = get_schema_view(
    openapi.Info(
        title="Finance Tracker User",
        default_version='v1',
        description="API for track your incomes and outcomes",
        contact=openapi.Contact(email="oo1amirmuhammad@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', UserView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]