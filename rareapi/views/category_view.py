from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CategoryView(ViewSet):
    """Rare categories view"""

    def retrieve(self, request, pk):
        try: 
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"message": "Category does not exist"}, status = status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        categories = Category.objects.all().order_by('label')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        category = Category.objects.create(
            label=request.data["label"]
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def update(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Category
        fields = ('id', 'label', )