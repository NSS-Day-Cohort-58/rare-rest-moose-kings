from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, RareUser, Reaction, PostReaction


class PostReactionView(ViewSet):
    """Rare postreaction view"""

    def create(self, request):
        
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data['post_id'])
        reaction = Reaction.objects.get(pk=request.data['reaction_id'])
        postreaction = PostReaction.objects.create(
            user=user,
            post=post,
            reaction=reaction,
            )
        serializer = PostReactionSerializer(postreaction)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class PostReactionSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PostReaction
        fields = ('id', 'user', 'post', 'reaction', )