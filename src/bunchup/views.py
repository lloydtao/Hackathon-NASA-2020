from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Hub, Activity, Membership, Room
from .forms import ImageUploadForm

class HomeView(ListView):
    model = Hub
    template_name = 'bunchup/index.html'
    context_object_name = 'hubs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["highlights"] = {}

        featured = Hub.objects.all()
        context["highlights"]["Featured"] = featured

        minecraft_activities = Activity.objects.filter(tags__title__contains="minecraft")
        context["highlights"]["Minecraft"] = minecraft_activities

        skribbl_activities = Activity.objects.filter(tags__title__contains="skribbl.io")
        context["highlights"]["Skribbl.io"] = skribbl_activities

        activities = Activity.objects.all()
        context["highlights"]["Activities"] = activities

        return context
    

class HubView(DetailView):
    model = Hub
    
    def get_context_data(self, **kwargs):
        context = super(HubView, self).get_context_data(**kwargs)
        hub = self.get_object()
        members = hub.membership_set.filter()
        admins = []
        for member in members:
            if member.is_admin:
                admins.append(member.user)
        context['admins'] = admins
        return context

class HubCreateView(LoginRequiredMixin, CreateView):
    model = Hub
    form_class = ImageUploadForm

    def form_valid(self, form):
        self.object = form.save()
        Membership.objects.create(
            user=self.request.user,
            hub=self.object,
            is_admin=True
        )
        return HttpResponseRedirect(reverse_lazy("bunchup-hub", kwargs={"pk": str(self.object.pk)}))


class HubUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hub
    form_class = ImageUploadForm
    context_object_name = 'hubs'
    template_name = 'bunchup/hub_update.html'

    def test_func(self):
        hub = self.get_object()
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False


class HubDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Hub
    success_url = '/'
        
    def test_func(self):
        hub = self.get_object()
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False


class ActivityView(DetailView):
    model = Activity
    template_name = 'bunchup/activity.html'
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        context = super(ActivityView, self).get_context_data(**kwargs)
        activity = self.get_object()

        context["chat_messages"] = activity.room.messages.all()

        return context


class ActivityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Activity
    context_object_name = 'activities'
    fields = ['name', 'description', 'start_date', 'finish_date']

    def form_valid(self, form):
        self.object = form.save()
        pk = self.kwargs['pk']
        self.object.hub = Hub.objects.get(pk=pk)
        self.object.users.add(self.request.user)
        room = Room(name=self.object.name,
                    description=self.object.description,
                    hub=self.object.hub,
                    activity_room=True
                    )
        room.save()
        self.object.room = room
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("bunchup-activity", kwargs={"pk": str(self.object.pk)}))

    def test_func(self):
        hub = Hub.objects.get(pk=self.kwargs['pk'])
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False


class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Activity
    success_url = "/"

    def test_func(self):
        hub = self.object.hub
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False


class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Hub
    context_object_name = 'hubs'
    template_name = 'bunchup/activity_update.html'
    fields = ['name', 'description', 'tags', 'start_date', 'finish_date', 'image']

    def test_func(self):
        hub = self.get_object()
        if hub.membership_set.filter(user=self.request.user).exists():
            return hub.membership_set.get(user=self.request.user).is_admin
        else:
            return False


class ActivityJoinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs['pk'])
        activity.users.add(self.request.user)
        activity.save()
        return HttpResponseRedirect(reverse_lazy("bunchup-activity", kwargs={"pk": str(activity.pk)}))


class HubJoinView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        hub = Hub.objects.get(pk=kwargs['pk'])
        hub.users.add(self.request.user)
        hub.save()
        return HttpResponseRedirect(reverse_lazy("bunchup-hub", kwargs={"pk": str(hub.pk)}))


class HubLeaveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        hub = Hub.objects.get(pk=kwargs['pk'])
        hub.users.remove(self.request.user)
        hub.save()
        return HttpResponseRedirect(reverse_lazy("bunchup-hub", kwargs={"pk": str(hub.pk)}))


class ActivityLeaveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs['pk'])
        activity.users.remove(self.request.user)
        activity.save()
        return HttpResponseRedirect(reverse_lazy("bunchup-activity", kwargs={"pk": str(activity.pk)}))