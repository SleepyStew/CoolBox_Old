from django.db import models

# Create your models here.


class Reminder(models.Model):
    title = models.CharField(max_length=48)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('schoolboxauth.User', on_delete=models.CASCADE)
    display_id = models.IntegerField(default=0)
    repeat = models.IntegerField(default=0)
    due = models.IntegerField(default=0)
