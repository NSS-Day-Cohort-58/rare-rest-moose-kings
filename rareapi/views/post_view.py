"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rareapi.models import Post, RareUser, Category
from django.contrib.auth.models import User
from datetime import date


class PostView(ViewSet):
    """Rare Posts view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """

        post = Post.objects.get(pk=pk)


        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all Posts

        Returns:
            Response -- JSON serialized list of Posts
        """

        filtered_posts = Post.objects.all()


        if "user" in request.query_params:
            query_value = request.query_params["user"]
            token = Token.objects.get(key=query_value)
            user_id = token.user_id
            filtered_posts = filtered_posts.filter(user=user_id)

        if "category" in request.query_params:
            query_value = request.query_params["category"]
            filtered_posts = filtered_posts.filter(category=query_value)

            serializer = PostSerializer(filtered_posts, many=True)


        serializer = PostSerializer(filtered_posts, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized Post instance
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data["category"])


        post = Post.objects.create(
            user=rare_user,
            category=category,
            title=request.data["title"],
            publication_date=date.today(),
            image_url=request.data["image_url"],
            content=request.data["content"],
            approved=True,
    )

        serializer = PostSerializer(post)
        return Response(serializer.data)


    def update(self, request, pk):
        """Handle PUT requests for a Post

        Returns:
        Response -- Empty body with 204 status code
            """

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.imageUrl = request.data["image_url"]
        post.content = request.data["content"]

        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)







class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "label",)

class PostSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=False)

    class Meta:
        model = Post
        fields = ("id", "user", "category", "title", "publication_date", "image_url", "content", "approved",)