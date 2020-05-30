from django.urls import path
from .views import HomeView, HubView, HubCreateView, HubUpdateView, ActivityView, ActivityCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='bunchup-home'),
    path('hub/<int:pk>', HubView.as_view(), name='bunchup-hub'),
    path('hub_edit/<int:pk>', HubUpdateView.as_view(), name='bunchup-hub-update'),
    path('activity/<str:username>', ActivityView.as_view(), name='bunchup-activity'),
    path('create/hub/', HubCreateView.as_view(), name='bunchup-hub-create'),
    path('create/activity/', ActivityCreateView.as_view(), name='bunchup-activity-create'),
]
