from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Challenge, Friendship, BingoGrid, TileInteraction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # custom order of fields
    fields = ("username", "first_name", "last_name", "bio", "total_points", "email", "birthdate",
              "visibility", "avatar", "gender_identity", "indigenous_identity", "last_login", "is_active", "is_superuser", "password")

    list_display = ("username", "first_name", "last_name", "total_points", "email", "birthdate",
                    "visibility", "avatar", "gender_identity", "indigenous_identity", "is_superuser", "is_active")

    def save_model(self, request, obj, form, change):
        if obj.pk is not None:  # Existing user
            original_obj = self.model.objects.get(pk=obj.pk)
            if obj.password == original_obj.password:
                # Password hasn't changed, no need to rehash
                obj.password = original_obj.password
            else:
                # Password has changed, rehash the new password
                obj.set_password(obj.password)
        else:
            # New user, hash the password
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'description', 'challenge_type',
              'points', 'total_completions')
    readonly_fields = ('total_completions', 'id')

    list_display = fields


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('requester', 'receiver', 'status')
    fields = list_display


@admin.register(BingoGrid)
class BingoGridAdmin(admin.ModelAdmin):
    # disable the export2csv action
    def get_actions(self, request):
        actions = super().get_actions(request)
        return {k: v for k, v in actions.items() if k != 'csv_export_selected'}


@admin.register(TileInteraction)
class TileInteractionAdmin(admin.ModelAdmin):
    fields = ('user', 'grid', 'position', 'description', 'image', 'completed',
              'consent', 'date_started', 'date_completed', 'image_display')
    readonly_fields = ('image_display', 'date_started')

    list_display = ('user', 'grid', 'position', 'completed',
                    'consent', 'date_started', 'date_completed')

    def image_display(self, obj):
        return obj.get_image_html()


admin.site.unregister(Group)
