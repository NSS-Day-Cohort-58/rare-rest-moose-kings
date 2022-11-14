from django.db import models

class Reaction(models.Model):

    label = models.CharField(max_length=50)
    emoji = models.CharField(max_length=50)