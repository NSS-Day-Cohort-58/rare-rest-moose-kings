from django.db import models
from datetime import date

class Post(models.Model):

    user = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = date.today()
    image_url = models.TextField()
    content = models.TextField()
    approved = models.BooleanField()