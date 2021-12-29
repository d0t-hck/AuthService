from django.db.models.base import Model
from rest_framework import fields, serializers
from .models import User, Role, Code, Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

class PostUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    role = serializers.IntegerField(default=1)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ['url', 'user', 'acces_token', 'refresh_token']

class CodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Code
        fields = ['url', 'code', 'user', 'is_used']
