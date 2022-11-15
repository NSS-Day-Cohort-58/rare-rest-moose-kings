from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser

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
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        post = Post.objects.get(pk=request.data['post'])
        author = RareUser.objects.get(pk=request.data['rareuser'])
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=request.data['content'],
            created_on=request.data['created_on'],
            )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.post = Post.objects.get(pk=request.data['post'])
        comment.author = RareUser.objects.get(user=request.auth.user)
        comment.created_on = request.data['created_on']
        comment.content = request.data['content']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CommentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on' )