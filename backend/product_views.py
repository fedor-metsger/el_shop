
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from backend.models import Contact, Product

class ProductDetailView(DetailView):
    model = Product

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data["moderator"] = "moderator" in [i.name for i in self.request.user.groups.all()]
    #     return context_data