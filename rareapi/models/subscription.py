from django.db import models
from datetime import date

class Subscription(models.Model):

    follower = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    author = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    created_on = date.today()
    ended_on = date.today()