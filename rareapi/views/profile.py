from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser
from django.contrib.auth.models import User

class ProfileView(ViewSet):



    def list(self, request):  
        rareusers = RareUser.objects.all()

        
        rareuser = RareUserSerializer(
            rareusers, many=True, context={'request': request}
        )

        
        return Response(rareuser.data)


        
class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'is_staff')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RareUser
        fields= ('profile_image_url', 'bio', 'created_on', 'user')