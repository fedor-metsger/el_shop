
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from frontend.forms import ProductUpdateForm, ProductListForm, BasketListForm


class ProductListView(TemplateView):
    form_class = ProductListForm
    template_name = 'frontend/product_list.html'


class ProductUpdateView(TemplateView):
    form_class = ProductUpdateForm
    success_url = reverse_lazy("backend:product")
    template_name = 'frontend/product_update.html'


class BasketListView(TemplateView):
    form_class = BasketListForm
    template_name = "frontend/basket.html"

class ContactListView(TemplateView):
    # form_class = ClientListForm
    template_name = "frontend/contact_list.html"

class OrderListView(TemplateView):
    # form_class = ClientListForm
    template_name = "frontend/order_list.html"
