from django.db import models

# Create your models here.


class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('schoolboxauth.User', on_delete=models.CASCADE)
    display_id = models.IntegerField(default=0)