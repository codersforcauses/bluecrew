from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import BingoGrid, Challenge, TileInteraction
from datetime import date

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birthdate',
                  'password', 'indigenous_identity', 'gender_identity']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        validated_data["is_active"] = False
        user = User.objects.create_user(
            **validated_data
        )
        return user

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_birthdate(self, value):
        if value and value > date.today():
            raise serializers.ValidationError(
                'Birth date cannot be in the future.')
        return value

    def validate_username(self, value):
        name = value.replace('_', '')
        if not name.isalnum():
            raise serializers.ValidationError(
                'Usernames can only contain alphanumeric characters or "_".'
            )
        return value

    # Front end sends empty strings if form is empty, but serializer will interpret this a string.
    # Similarly, first_name and last_name are sent as empty string if the form is not filled.
    # We want to interpret this as no value given, not as a string.
    def to_internal_value(self, data):
        if data.get('birthdate', None) == '':
            data.pop('birthdate')
        if data.get('first_name', None) == '':
            data.pop('first_name')
        if data.get('last_name', None) == '':
            data.pop('last_name')
        return super(UserRegisterSerializer, self).to_internal_value(data)


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


class UpdatePreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar", "bio", "visibility"]


class ProfilePageChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ["name", "description", "challenge_type",
                  "points"]

    def to_representation(self, instance):
        # This ensures the field names match the TypeScript interface
        data = super().to_representation(instance)
        data["type"] = data.pop("challenge_type").capitalize()
        data["title"] = data.pop("name")
        return data


class ProfilePageTileSerializer(serializers.ModelSerializer):
    date_started = serializers.DateTimeField(format="%d/%m/%y %I:%M %p")
    date_completed = serializers.DateTimeField(format="%d/%m/%y %I:%M %p")

    class Meta:
        model = TileInteraction
        fields = ("image", "date_started", "date_completed",
                  "completed", "description")

    def to_representation(self, instance):
        # This ensures the field names match the TypeScript interface
        data = super().to_representation(instance)
        data["finishDate"] = data.pop("date_completed")
        data["startDate"] = data.pop("date_started")
        possibly_blank_description = data.pop("description")
        if possibly_blank_description:
            data["imageDescription"] = possibly_blank_description
        return data


class ProfilePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "bio",
                  "total_points", "avatar"]

    def to_representation(self, instance):
        # This ensures the field names match the TypeScript interface
        data = super().to_representation(instance)
        data["firstName"] = data.pop("first_name")
        data["lastName"] = data.pop("last_name")
        data["totalPoints"] = data.pop("total_points")
        return data


class ChallengeCompleteSerializer(serializers.ModelSerializer):
    # Serializer for completing challenge view.
    class Meta:
        model = TileInteraction
        fields = ['position', 'consent', 'image', 'description']
        extra_kwargs = {
            'position': {'required': True},
            'consent': {'required': True},
            'description': {'required': False,
                            'allow_blank': True,
                            # need to specify maximum length since the length of a textfield is not enforced on the db level
                            'max_length': 500}

        }


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'user_id']


class UpdateBingoGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = BingoGrid
        fields = ('challenges', )

    def validate_challenges(self, value):
        if len(value) != 16 or len(set(value)) != 16:
            raise serializers.ValidationError(
                "You must provide the ids of exactly 16 distinct challenges.")
        return value


class FriendshipUserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id')
    userName = serializers.CharField(source='username')
    friendship_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['userId', 'userName', 'avatar', 'friendship_id']

    def get_friendship_id(self, obj):
        friendship = self.context.get('friendship')
        return friendship.id if friendship else None
