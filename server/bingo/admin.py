from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Challenge, Friendship, BingoGrid, TileInteraction


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    # custom order of fields
    fields = ("username", "first_name", "last_name", "bio", "total_points", "email", "birthdate",
              "visibility", "avatar", "gender_identity", "indigenous_identity", "last_login", "is_active", "is_superuser", "password")

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


admin.site.register(Friendship)
admin.site.register(BingoGrid)


@admin.register(TileInteraction)
class TileInteractionAdmin(admin.ModelAdmin):
    readonly_fields = ('image_display',)

    def image_display(self, obj):
        return obj.get_image_html()


admin.site.unregister(Group)
