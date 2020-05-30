from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 320 or img.width > 320:
            size = (300, 300)
            img.thumbnail(size, Image.ANTIALIAS)
            img.save(self.image.path)
