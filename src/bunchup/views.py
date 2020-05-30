from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Hub, Activity

class HomeView(ListView):
    model = Hub
    template_name = 'bunchup/index.html'
    context_object_name = 'hubs'

class HubView(DetailView):
    model = Hub
    template_name = 'bunchup/hub.html'
    context_object_name = 'hubs'
    
class HubCreateView(LoginRequiredMixin, CreateView):
    model = Hub
    context_object_name = 'hubs'
    fields = ['name', 'description', 'locked', 'tags']
    
class ActivityView(DetailView):
    model = Activity
    template_name = 'bunchup/activity.html'
    context_object_name = 'activities'
    
class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    context_object_name = 'activities'
    fields = ['name', 'description']
