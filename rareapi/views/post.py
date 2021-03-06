# from django.contrib.auth.models import User
from rareapi.models.category import Category
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from rareapi.models import Post, RareUser, Category, Tag
from datetime import date


class PostView(ViewSet):
    """Levelposts"""

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.user = user

        category = Category.objects.get(pk=request.data["category"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """
        user = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.publication_date = date.today()
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.tags = request.data["tags"]
        post.user = user

        category = Category.objects.get(pk=request.data["category"])
        post.category = category
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status post
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.all()
        posts.rare_user = rare_user

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=["PUT"], detail=True)
    
    # @action decorator is adding a new route that accepts PUT requests and adds postId to the url.
    # /posts/1/update_tag
    def update_tag(self, request, pk):
        post = Post.objects.get(pk=pk)
        # Get single post
        post.tags.add(request.data["tag"])
        # Setting tag data being sent from the front end.
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'label']

class RareUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RareUser
        fields = ['id', 'user', 'bio', 'profile_image_url', 'active', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):

    user = RareUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ['id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'comment_set']
        depth = 1