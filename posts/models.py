from django.db import models

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)