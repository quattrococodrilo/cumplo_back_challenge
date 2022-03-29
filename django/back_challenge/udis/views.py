from re import template

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from udis.forms import UdisForm


class UdisFormView(FormView):

    template_name = 'udis/index.html'
    form_class = UdisForm
    success = reverse_lazy('udis:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["udis"] = []
        return context
