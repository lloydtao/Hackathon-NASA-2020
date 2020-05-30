from django.contrib import admin
from .models import Tag, Activity, Hub, Room, Message, Membership

# Register your models here.
admin.site.register(Tag)
admin.site.register(Activity)
admin.site.register(Hub)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Membership)
