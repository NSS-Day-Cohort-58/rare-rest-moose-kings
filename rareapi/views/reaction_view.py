from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import Reaction

class ReactionView(ViewSet):

    def retrieve(self, request, pk):

        reaction = Reaction.objects.get(pk=pk)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)


    def list(self, request):

        reaction = Reaction.objects.all()
        serializer = ReactionSerializer(reaction, many=True)
        return Response(serializer.data)


    def create(self, request):

        reaction = Reaction.objects.create(
            label = request.data["label"],
            emoji = request.data["emoji"]
        )
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)


    def update(self, request, pk):

        reaction = Reaction.objects.get(pk=pk)
        reaction.label = request.data["label"]
        reaction.emoji = request.data["emoji"]
        reaction.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'emoji',)