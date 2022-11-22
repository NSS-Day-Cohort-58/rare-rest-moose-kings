from django.db import models
from datetime import date

class Post(models.Model):

    user = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField(default=date.today)
    image_url = models.TextField()
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through='PostTag', related_name='tags')

    @property
    def postreaction_count(self):
        return self.__postreaction_count

    @postreaction_count.setter
    def postreaction_count(self, value):
        self.__postreaction_count = value
