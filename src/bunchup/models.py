from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from tagging.registry import register
from tagging.fields import TagField

from PIL import Image

def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)
    
    
class Tag(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class Hub(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    locked = models.BooleanField(default=False)
    # tags = models.ManyToManyField(Tag, blank=True)
    tags = TagField()
    users = models.ManyToManyField(User, through='Membership', blank=True)
    image = models.ImageField(default='default-hub.png', upload_to='hub_pics')

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        target_width = 346
        target_height = 216

        if img.height > target_height or img.width > target_width:
            size = (target_width, target_height)
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(self.image.path)

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=True)
    room = models.OneToOneField('Room', on_delete=models.CASCADE, null=True, blank=True)
    tags = TagField()
    start_date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(default=one_day_hence())
    users = models.ManyToManyField(User, blank=True)
    image = models.ImageField(default='default-activity.png', upload_to='activity_pics')

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        target_width = 346
        target_height = 216

        if img.height > target_height or img.width > target_width:
            size = (target_width, target_height)
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(self.image.path)


    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    activity_room = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_length=1024)
    # on_delete => Set to null user. Message remains after account deletion.
    owner = models.ForeignKey(User, on_delete=models.SET(0))
    date_time = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str('%s %s %s %s %s %s' % ("Hub:", self.hub, "| Member:", self.user, "| Admin:", self.is_admin))
