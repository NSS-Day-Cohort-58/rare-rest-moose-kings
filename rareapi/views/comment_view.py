from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser
from datetime import date

class CommentView(ViewSet):
    """Rare comments view"""

    def retrieve(self, request, pk):
        try: 
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({"message": "Comment does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        comments = Comment.objects.all()
        
        if "posts" in request.query_params:
            query_value = request.query_params["posts"]
            comments = comments.filter(post_id=query_value).order_by('created_on')

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        post = Post.objects.get(pk=request.data['post'])
        author = RareUser.objects.get(user=request.auth.user)
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=request.data['content'],
            created_on=date.today(),
            )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.post = Post.objects.get(pk=request.data['post'])
        comment.author = RareUser.objects.get(user=request.auth.user)
        comment.created_on = date.today()
        comment.content = request.data['content']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('username', )


class CommentSerializer(serializers.ModelSerializer):
   
    author = RareUserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on', )