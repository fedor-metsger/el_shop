
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView


class ProductListView(TemplateView):
    template_name = 'frontend/product_list.html'


class ProductUpdateView(TemplateView):
    success_url = reverse_lazy("backend:product")
    template_name = 'frontend/product_update.html'


class BasketListView(TemplateView):
    template_name = "frontend/basket.html"

class ContactListView(TemplateView):
    template_name = "frontend/contact_list.html"

class OrderListView(TemplateView):
    template_name = "frontend/order_list.html"
