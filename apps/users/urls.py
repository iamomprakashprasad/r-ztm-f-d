from django.urls import path
from .views import RegisterView, LoginView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("users/", UserListView.as_view(), name="user-list"),
]
