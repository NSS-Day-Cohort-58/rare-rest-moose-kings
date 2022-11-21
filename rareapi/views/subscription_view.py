from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import Subscription, RareUser
from datetime import date
from rest_framework.authtoken.models import Token



class SubscriptionView(ViewSet):

    def retrieve(self, request, pk):

        subscription = Subscription.objects.get(pk=pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)


    def list(self, request):
        
        subscription = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)


    def create(self, request):

        author = RareUser.objects.get(pk=request.data["author"])
        token = request.data["follower"]
        token_user = Token.objects.get(key=token)
        follower = RareUser.objects.get(user=token_user.user_id)

        subscription = Subscription.objects.create(
            follower = follower,
            author = author,
            created_on = date.today(),
            ended_on = None
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def update(self, request, pk):
        
        author = RareUser.objects.get(pk=request.data["author"])
        follower = RareUser.objects.get(pk=request.data["follower"])
        
        subscription = Subscription.objects.get(pk=pk)
        subscription.follower = follower
        subscription.author = author
        subscription.created_on = request.data["created_on"]
        subscription.ended_on = date.today()
        subscription.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', 'tokenNumber', )
        

class SubscriptionSerializer(serializers.ModelSerializer): 
    follower = RareUserSerializer(many=False)
    
    class Meta:
        model = Subscription
        fields = ('id', 'follower', 'author', 'created_on', 'ended_on', )