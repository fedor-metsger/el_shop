
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shop.api_views import UserViewSet, PartnerUpdate
from shop.shop_views import ProductUpdateView
from shop.user_views import LoginView, LogoutView, UserRegisterView, UserPasswordView
from shop.product_views import ProductListView

app_name = "backend"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    # path("activation/<int:pk>/", UserActivationView.as_view(), name="activation"),
    # path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("password_reset/", UserPasswordView.as_view(), name="password"),

    path("user/login/", TokenObtainPairView.as_view(), name="token_obtain"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/register/", UserViewSet.as_view({"post": "create"}), name="user_register"),
    path("user/password_reset/", UserViewSet.as_view({"patch": "partial_update"}), name="reset_password"),

    path("", ProductListView.as_view(), name="product"),
    path("product/update/", ProductUpdateView.as_view(), name="product_update"),

    path("partner/update/", PartnerUpdate.as_view(), name="partner_update"),
]