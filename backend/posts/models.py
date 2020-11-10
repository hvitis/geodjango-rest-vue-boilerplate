from django.db import models

class Post(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
