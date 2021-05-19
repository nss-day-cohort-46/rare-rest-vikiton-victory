"""View module for handling requests about category types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category, RareUser
from rest_framework import status, viewsets



class CategoryView(ViewSet):
    def create(self, request):
        """Handle category operations

        Returns:
            Response -- JSON serialized category instance
        """

        category = Category()
        category.label = request.data["label"]

        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)




    def retrieve(self, request, pk=None):
        """Handle GET requests for single category type

        Returns:
            Response -- JSON serialized category type
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all category types

        Returns:
            Response -- JSON serialized list of category types
        """
        categories = Category.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category types

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')