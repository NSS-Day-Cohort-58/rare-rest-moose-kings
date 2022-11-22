from django.db import models

class PostReaction(models.Model):

    user = models.ForeignKey('RareUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    reaction = models.ForeignKey('Reaction', on_delete=models.CASCADE)

    @property
    def count(self):
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
