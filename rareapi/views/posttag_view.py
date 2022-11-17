from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Post, PostTag, Tag


class PostTagView(ViewSet):
    """Rare posttag view"""

    def create(self, request):
        post = Post.objects.get(pk=request.data['post_id'])
        tag = Tag.objects.get(pk=request.data['tag_id'])
        posttag = PostTag.objects.create(
            post=post,
            tag=tag,
            )
        serializer = PostTagSerializer(posttag)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

class PostTagSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PostTag
        fields = ('id', 'post', 'tag', )