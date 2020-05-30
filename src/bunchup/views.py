from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Hub, Activity

class HomeView(ListView):
    model = Hub
    template_name = 'bunchup/index.html'
    context_object_name = 'hubs'

class HubView(DetailView):
    model = Hub

class HubCreateView(LoginRequiredMixin, CreateView):
    model = Hub
    context_object_name = 'hubs'
    fields = ['name', 'description', 'locked', 'tags']

class HubUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hub
    context_object_name = 'hubs'
    template_name = 'bunchup/hub_update.html'
    fields = ['name', 'description', 'locked', 'tags']
    
    def test_func(self):
        hub = self.get_object()
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False





class ActivityView(DetailView):
    model = Activity
    template_name = 'bunchup/activity.html'
    context_object_name = 'activities'


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    context_object_name = 'activities'
    fields = ['name', 'description', 'start_date', 'finish_date']
