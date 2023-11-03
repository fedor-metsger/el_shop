
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend.views import UserViewSet, PartnerUpdate, CategoryView, ShopView, ProductInfoView, \
    ProductSimpleView, BasketView, OrderView, ContactView
from frontend.views import ProductUpdateView, ProductListView, BasketListView, ContactListView, OrderListView
from backend.user_views import LoginView, LogoutView, UserRegisterView, UserPasswordView

app_name = "frontend"

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("contact_list/", ContactListView.as_view(), name="contact-list"),
    path("basket_edit/", BasketListView.as_view(), name="basket-edit"),
    path("order_list/", OrderListView.as_view(), name="order-list"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("price_update/", ProductUpdateView.as_view(), name="product-update"),

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("activation/<int:pk>/", UserActivationView.as_view(), name="activation"),
    # path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("password_reset/", UserPasswordView.as_view(), name="password"),
]