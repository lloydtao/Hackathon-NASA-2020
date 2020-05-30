from django.shortcuts import render
from django.views.generic import ListView
from .models import Hub

class HomeView(ListView):
    model = Hub
    template_name = 'bunchup/index.html'
