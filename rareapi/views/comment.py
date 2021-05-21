from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, RareUser, Post
from django.contrib.auth.models import User
from datetime import datetime

class CommentView(ViewSet):
    def create(self, request):
        """Handle POST operations for comments
        Returns:
            Response -- JSON serialized comment instance
        """
        # Uses the token passed in the `Authorization` header
        # post = Post()
        author = RareUser.objects.get(user = request.auth.user) 
        # Create a new Python instance of the comment class
        # and set its properties from what was sent in the
        # body of the request from the client.
        comment = Comment()
        comment.post_id = request.data["post_id"]
        comment.content = request.data["content"]
        comment.author = author
        comment.created_on = datetime.now()
        # comment.content = request.data["content"]

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):  
        comments = Comment.objects.all()


        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):


        comment = Comment.objects.get(pk=pk)
        comment.label = request.data["label"]
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')