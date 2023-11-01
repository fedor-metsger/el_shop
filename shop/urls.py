
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from shop.api_views import UserViewSet, PartnerUpdate, CategoryView, ShopView, ProductInfoView, \
    ProductSimpleView, BasketView, OrderView, ContactView
from shop.html_views import ProductUpdateView, ProductListView, BasketListView, ContactListView
from shop.user_views import LoginView, LogoutView, UserRegisterView, UserPasswordView

app_name = "backend"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    # path("activation/<int:pk>/", UserActivationView.as_view(), name="activation"),
    # path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("password_reset/", UserPasswordView.as_view(), name="password"),
    path("basket_edit/", BasketListView.as_view(), name="basket-edit"),
    path("contact_list/", ContactListView.as_view(), name="contact-list"),

    path("api/v1/user/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/user/register/", UserViewSet.as_view({"post": "create"}), name="user-register"),
    path("api/v1/user/password_reset/", UserViewSet.as_view({"patch": "partial_update"}), name="password-reset"),
    path("api/v1/user/contact/", ContactView.as_view(), name="user-contact"),

    path("", ProductListView.as_view(), name="product-list"),
    path("price_update/", ProductUpdateView.as_view(), name="product-update"),

    path("api/v1/partner/update/", PartnerUpdate.as_view(), name="partner-update"),
    path("api/v1/categories/", CategoryView.as_view(), name="categories"),
    path("api/v1/shops/", ShopView.as_view(), name="shops"),
    path("api/v1/products/", ProductInfoView.as_view(), name="products"),
    path("api/v1/products_simple/", ProductSimpleView.as_view(), name="products-simple"),
    path("api/v1/basket/", BasketView.as_view(), name="basket"),
    path("api/v1/order/", OrderView.as_view(), name="order"),
]
