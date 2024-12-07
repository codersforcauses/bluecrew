from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, firstName, lastName, birthdate, password=None):

        user = self.model(
            username,
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
            birthdate=birthdate
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, firstName, lastName, birthdate, password=None):
        user = self.create_user(
            username,
            email=email,
            firstName=firstName,
            lastName=lastName,
            birthdate=birthdate
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ["firstName", "lastName", "birthdate", "email"]

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
        blank=False,
        default=0
    )
    avatar = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username
