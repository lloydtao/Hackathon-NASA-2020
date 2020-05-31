# forms.py
from django import forms
from .models import Hub

# from tagging import fields as tagfields

class ImageUploadForm(forms.ModelForm):
    # tags = tagfields.TagField()

    class Meta:
        model = Hub
        fields = ['name', 'description', 'locked', 'tags', 'image']