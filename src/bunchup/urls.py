from django.urls import path
from .views import HomeView, HubView, HubCreateView, ActivityView, ActivityCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='bunchup-home'),
    path('hub/<str:username>', HubView.as_view(), name='bunchup-hub'),
    path('activity/<str:username>', ActivityView.as_view(), name='bunchup-activity'),
    path('create/hub/', HubCreateView.as_view(), name='bunchup-hub-create'),
    path('create/activity/', ActivityCreateView.as_view(), name='bunchup-activity-create'),
]
