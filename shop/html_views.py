from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from shop.forms import ProductUpdateForm, ProductListForm, BasketListForm
from shop.models import Contact


class ProductListView(TemplateView):
    form_class = ProductListForm
    template_name = 'shop/product_list.html'


class ProductUpdateView(TemplateView):
    form_class = ProductUpdateForm
    success_url = reverse_lazy("backend:product")
    template_name = 'shop/product_update.html'


class BasketListView(TemplateView):
    form_class = BasketListForm
    template_name = "shop/basket.html"

class ContactListView(TemplateView):
    # form_class = ClientListForm
    template_name = "shop/contact_list.html"
