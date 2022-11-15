from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import RareUser

class RareUserView(ViewSet):

    def retrieve(self, request, pk):

        rare_user = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)


    def list(self, request):

        rare_user = RareUser.objects.all()
        serializer = RareUserSerializer(rare_user, many=True)
        return Response(serializer.data)


    def update(self, request, pk):

        rare_user = RareUser.objects.get(pk=pk)
        
        rare_user.bio = request.data["bio"]
        rare_user.profile_image_url = request.data["profile_image_url"]
        rare_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        rare_user = RareUser.objects.get(pk=pk)
        rare_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'profile_image_url', )