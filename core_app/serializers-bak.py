from django.contrib.auth.models import User
from .models import BoardList, Board, Card
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from core_app.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# samples
class SnippetSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']

# user serializer
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']








# trello
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User 
        fields = ('username', 'password')
    
    def validate(self, data):
        """
        Validate the inputed data
        """

        username, password = data.values()
        user = authenticate(username=username, password=password)

        # if user is invalid 
        if user is None:
            raise serializers.ValidationError("Invalid details")
        # return if user is valid
        return data

class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User 
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class BoardSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'archive']


class ListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardList
        fields = ['id', 'title', 'description', 'archive']


class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'archive']