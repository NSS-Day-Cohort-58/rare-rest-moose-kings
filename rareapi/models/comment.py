from django.db import models
from datetime import date

class Comment(models.Model):

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField(default=date.today)