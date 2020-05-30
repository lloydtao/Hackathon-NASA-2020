from django.db import models

class Hub(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
