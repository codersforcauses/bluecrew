# Generated by Django 5.1 on 2025-02-12 13:21

import datetime
import django.db.models.deletion
import sortedm2m.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Challenge",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "challenge_type",
                    models.CharField(
                        choices=[
                            ("connect", "Connect"),
                            ("understand", "Understand"),
                            ("act", "Act"),
                        ],
                        max_length=10,
                    ),
                ),
                ("points", models.PositiveIntegerField()),
                ("total_completions", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=30, unique=True)),
                ("first_name", models.CharField(blank=True, max_length=30)),
                ("last_name", models.CharField(blank=True, max_length=30)),
                ("bio", models.CharField(blank=True, max_length=300)),
                ("total_points", models.IntegerField(default=0)),
                ("birthdate", models.DateField(default=datetime.date(2000, 1, 1))),
                ("email", models.EmailField(max_length=320, unique=True)),
                (
                    "visibility",
                    models.IntegerField(
                        choices=[
                            (2, "Public"),
                            (1, "Friends Only"),
                            (0, "BlueCrew Only"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "gender_identity",
                    models.IntegerField(
                        choices=[
                            (0, "Male"),
                            (1, "Female"),
                            (2, "Non-Binary"),
                            (3, "Other"),
                            (4, "Prefer not to say"),
                        ],
                        default=4,
                    ),
                ),
                (
                    "indigenous_identity",
                    models.IntegerField(
                        choices=[(0, "Prefer not to say"), (1, "Yes"), (2, "No")],
                        default=0,
                    ),
                ),
                (
                    "avatar",
                    models.IntegerField(
                        choices=[
                            (0, "Avatar 0"),
                            (1, "Avatar 1"),
                            (2, "Avatar 2"),
                            (3, "Avatar 3"),
                            (4, "Avatar 4"),
                            (5, "Avatar 5"),
                        ],
                        default=0,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "ordering": ["-total_points", "username"],
            },
        ),
        migrations.CreateModel(
            name="BingoGrid",
            fields=[
                ("grid_id", models.AutoField(primary_key=True, serialize=False)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "challenges",
                    sortedm2m.fields.SortedManyToManyField(
                        help_text=None, to="bingo.challenge"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Friendship",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("accepted", "Accepted")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TileInteraction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveSmallIntegerField()),
                ("image", models.ImageField(blank=True, upload_to="challenge_images/")),
                ("completed", models.BooleanField(default=False)),
                ("consent", models.BooleanField(default=False)),
                ("date_started", models.DateTimeField(auto_now_add=True)),
                ("date_completed", models.DateTimeField(blank=True, null=True)),
                (
                    "grid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bingo.bingogrid",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["-total_points"], name="bingo_user_total_p_f1bcb7_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="friendship",
            constraint=models.UniqueConstraint(
                fields=("requester", "receiver"), name="unique_friendship"
            ),
        ),
        migrations.AddConstraint(
            model_name="tileinteraction",
            constraint=models.CheckConstraint(
                condition=models.Q(("position__lte", 15)), name="position_lte_15"
            ),
        ),
        migrations.AddConstraint(
            model_name="tileinteraction",
            constraint=models.UniqueConstraint(
                fields=("user", "grid", "position"), name="unique_user_grid_challenge"
            ),
        ),
    ]
