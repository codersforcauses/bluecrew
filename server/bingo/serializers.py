from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import BingoGrid, Challenge, TileInteraction

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    def validate_password(self, value):
        validate_password(value)
        return value


class LeaderboardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'total_points']


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
            'avatar'
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
            'avatar': data['avatar']
        }


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['name', 'description', 'challenge_type', 'points']


class BingoGridSerializer(serializers.ModelSerializer):
    challenges = ChallengeSerializer(read_only=True, many=True)

    class Meta:
        model = BingoGrid
        fields = ['grid_id', 'challenges']


class UpdatePreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar", "bio", "visibility"]


class ProfilePageChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ["name", "description", "challenge_type",
                  "points"]


class ProfilePageTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TileInteraction
        fields = ["image", "date_started", "date_completed"]


class ProfilePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio",
                  "total_points", "avatar"]
