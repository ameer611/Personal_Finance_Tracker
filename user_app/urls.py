from django.urls import path

from user_app.views import RegisterView, LoginView, UserView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserView.as_view()),
]