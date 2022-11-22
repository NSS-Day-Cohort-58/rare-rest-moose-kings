from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import RareUser, Subscription, Post
from django.contrib.auth.models import User

class RareUserView(ViewSet):

    def retrieve(self, request, pk):

        rare_user = RareUser.objects.get(pk=pk)
        subs = Subscription.objects.all()
        
        subs_list = []
        for sub in subs:
            if sub.author_id == rare_user.id:
                if sub.ended_on == None:
                    subs_list.append(sub)
                    rare_user.sub_count = len(subs_list)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)


    def list(self, request):
        

        rare_user = RareUser.objects.all().order_by('user__first_name')
        serializer = RareUserSerializer(rare_user, many=True)
        return Response(serializer.data)


    def update(self, request, pk):

        rare_user = RareUser.objects.get(pk=pk)
        user = User.objects.get(pk=rare_user.user_id)
        
        rare_user.bio = request.data["bio"]
        rare_user.profile_image_url = request.data["profile_image_url"]
        user.is_staff = request.data["is_staff"]
        user.is_active = request.data["is_active"]
        user.save()
        rare_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        rare_user = RareUser.objects.get(pk=pk)
        rare_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "is_staff", "date_joined", "email", "is_active")

class RareUserSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('id', 'user', "full_name", 'bio', 'profile_image_url', "tokenNumber", "sub_count",)