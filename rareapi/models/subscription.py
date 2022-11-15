from django.db import models
from datetime import date

class Subscription(models.Model):

    follower = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='author')
    created_on = models.DateField(default=date.today)
    ended_on = models.DateField(null=True)