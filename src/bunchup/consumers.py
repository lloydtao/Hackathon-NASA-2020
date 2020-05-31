import json
import random

from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Activity


class ChatConsumer(WebsocketConsumer):
    channels = {}

    def connect(self):
        self.user = self.scope["user"]

        # Generate a unique identity
        self.identity = None
        while self.identity is None or self.identity in self.channels:
            self.identity = random.randint(0, 100000000)

        # Add unique identity to message distribution network
        self.channels[self.identity] = self

        self.accept()

    def disconnect(self, close_code):
        del self.channels[self.identity]

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message.strip() == "":
            return

        activity = text_data_json["activity"]

        room = Activity.objects.get(id=activity).room

        model = Message(
            text=message,
            owner=self.user,
            room=room
        )
        model.save()


@receiver(post_save, sender=Message, dispatch_uid="react_new_message")
def react_new_message(sender, instance, **kwargs):
    for identity, channel in ChatConsumer.channels.items():
        channel.send(text_data=json.dumps({
            "text": instance.text,
            "owner": instance.owner.username,
            "picture": instance.owner.profile.image.url
        }))