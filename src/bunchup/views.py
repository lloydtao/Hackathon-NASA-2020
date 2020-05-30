from django.shortcuts import render
from django.views.generic import ListView

class HomeView(ListView):
    template_name = 'bunchup/index.html'
