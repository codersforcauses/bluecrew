from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ["username", "firstName", "lastName", "birthdate", "email", "visibility", "avatar"]

    userID = models.BigAutoField(primary_key=True)

    username = models.CharField(max_length=30, unique=True)
    USERNAME_FIELD = "username"

    firstName = models.CharField(max_length=30, blank=False)
    lastName = models.CharField(max_length=30, blank=False)
    bio = models.CharField(max_length=300)
    totalPoints = models.IntegerField(default=0)
    birthdate = models.DateField(blank=False)

    email = models.EmailField(
        max_length=320,
        unique=True,
        blank=False
    )
    EMAIL_FIELD = 'email'

    class Visibility(models.IntegerChoices):
        PUBLIC = (2, "Public")
        FRIENDS = (1, "Friends Only")
        BLUECREW = (0, "BlueCrew Only")
    visibility = models.IntegerField(
        choices=Visibility,
        blank=False
    )
    avatar = models.IntegerField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
