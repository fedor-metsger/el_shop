
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shop.user_views import LoginView, LogoutView, UserRegisterView, UserUpdateView, UserPasswordView, UserActivationView
from shop.product_views import ProductListView

app_name = "shop"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    # path("activation/<int:pk>/", UserActivationView.as_view(), name="activation"),
    # path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("password/<int:pk>/", UserPasswordView.as_view(), name="password"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("", ProductListView.as_view(), name="product"),
]