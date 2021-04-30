from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.

class Script(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False, blank=False)


class NewScriptForm(forms.Form):
    name = forms.CharField(max_length=50, label='Script Name')
    description = forms.CharField(label='Script Description')
    content = forms.CharField(label='Script Content', widget=forms.Textarea)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False, blank=False)