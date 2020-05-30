from django.urls import path
from .views import HomeView, HubView, HubCreateView, HubUpdateView, HubDeleteView, ActivityView, ActivityCreateView

urlpatterns = [
    path('', HomeView.as_view(), name='bunchup-home'),
    path('hub/<int:pk>/', HubView.as_view(), name='bunchup-hub'),
    path('hub/<int:pk>/edit/', HubUpdateView.as_view(), name='bunchup-hub-update'),
    path('hub/<int:pk>/delete/', HubDeleteView.as_view(), name='bunchup-hub-delete'),
    path('activity/<str:username>', ActivityView.as_view(), name='bunchup-activity'),
    path('create/hub/', HubCreateView.as_view(), name='bunchup-hub-create'),
    path('create/activity/', ActivityCreateView.as_view(), name='bunchup-activity-create'),
]
