from django.urls import reverse_lazy
from django.views.generic import TemplateView

from shop.forms import ProductUpdateForm


class ProductUpdateView(TemplateView):
    form_class = ProductUpdateForm
    success_url = reverse_lazy("backend:product")
    template_name = 'shop/product_update.html'
