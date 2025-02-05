from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import BingoGrid, Challenge, TileInteraction

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password', 'indigenous_identity', 'gender_identity']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value


class LeaderboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'total_points', 'avatar']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',       # maps to userId
            'username',      # maps to userName
            'first_name',    # maps to firstName
            'last_name',     # maps to lastName
            'bio',
            'total_points',  # maps to totalPoints
            'email',
            'visibility',
            'avatar',
            'is_superuser'
        ]

    def to_representation(self, instance):
        # This ensures the field names match the TypeScript interface
        data = super().to_representation(instance)
        return {
            'userId': data['user_id'],
            'userName': data['username'],
            'firstName': data['first_name'],
            'lastName': data['last_name'],
            'bio': data['bio'],
            'totalPoints': data['total_points'],
            'email': data['email'],
            'visibility': data['visibility'],
            'avatar': data['avatar'],
            'isSuperuser': data['is_superuser']
        }


class ChallengeSerializer(serializers.ModelSerializer):
    # Nested serializer for BingoGridSerializer
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'challenge_type', 'points']


class BingoGridSerializer(serializers.ModelSerializer):
    challenges = ChallengeSerializer(read_only=True, many=True)

    class Meta:
        model = BingoGrid
        fields = ['grid_id', 'challenges']


class UpdatePreferencesSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar", "bio", "visibility"]


class ChallengeCompleteSerializer(serializers.ModelSerializer):
    # Serializer for completing challenge view.
    class Meta:
        model = TileInteraction
        fields = ['position', 'consent', 'image']
        extra_kwargs = {
            'position': {'required': True},
            'consent': {'required': True},
        }
