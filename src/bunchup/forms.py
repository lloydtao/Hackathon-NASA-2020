# forms.py
from django import forms
from .models import Hub

class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = Hub
        fields = ['name', 'description', 'locked', 'tags', 'image']