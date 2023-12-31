
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
)

from backend.views import UserViewSet, PartnerUpdate, CategoryView, ShopView, ProductInfoView, \
    ProductSimpleView, BasketView, OrderView, ContactView, OrderDetailView

app_name = "backend"

urlpatterns = [
    path("user/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    # path("user/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/register/", UserViewSet.as_view({"post": "create"}), name="user-register"),
    path("user/password_reset/", UserViewSet.as_view({"patch": "partial_update"}), name="password-reset"),
    path("user/contact/", ContactView.as_view(), name="user-contact"),

    path("partner/update/", PartnerUpdate.as_view(), name="partner-update"),
    path("partner/update/<str:task_id>/", PartnerUpdate.as_view(), name="update-status"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("shops/", ShopView.as_view(), name="shops"),
    path("products/", ProductInfoView.as_view(), name="products"),
    path("products_simple/", ProductSimpleView.as_view(), name="products-simple"),
    path("basket/", BasketView.as_view(), name="basket"),
    path("order/", OrderView.as_view(), name="order"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-retrieve"),
]
