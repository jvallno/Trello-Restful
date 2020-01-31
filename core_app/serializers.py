from django.contrib.auth.models import User
from .models import BoardList, Board, Card, BoardInvite
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.mail import EmailMultiAlternatives



class UserSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User 
        fields = ('username', 'password')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User 
        fields = ('username', 'email', 'password', 'confirm_password')
    
    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BoardSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Board
        fields = ['id', 'title', 'description', 'owner', 'archive']


class ListSerializer(serializers.ModelSerializer):
    
    cards = serializers.SerializerMethodField()

    class Meta:
        model = BoardList
        fields = ['id', 'title', 'description', 'archive', 'cards']

    def get_cards(self, obj):
        card_obj = obj.card_set.all()
        serializer = CardSerializer(card_obj, many=True)
        return serializer.data


class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Card
        fields = ['id', 'title', 'description', 'archive']


class BoardInviteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoardInvite
        fields = ['member_email']