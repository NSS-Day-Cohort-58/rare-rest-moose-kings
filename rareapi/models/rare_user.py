from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image_url = models.TextField()
    
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'
    
    @property
    def tokenNumber(self):
        token = Token.objects.get(user_id=self.user.id)
        return f'{token}'