from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    title = models.CharField(max_length=32)


class Activity(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    room = models.OneToOneField('Room', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)


class Hub(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    locked = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    users = models.ManyToManyField(User, through='Membership', null=True, blank=True)


class Room(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    activity_room = models.BooleanField(default=False)


class Message(models.Model):
    text = models.CharField(max_length=1024)
    # on_delete => Set to null user. Message remains after account deletion.
    owner = models.ForeignKey(User, on_delete=models.SET(0))
    date_time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
