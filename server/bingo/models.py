from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    # userID
    # username
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(
        max_length=320,
        unique=True,
        blank=False
    )
    # passwordHash
    # bio
    # totalPoints
    # visibility
    # avatar
    pass
