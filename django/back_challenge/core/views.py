from re import template
from django.shortcuts import render

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """ Vista del home. """
    template_name = 'core/home.html'
