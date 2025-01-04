from django.contrib import admin
from .models import User, Challenge, Friendship, ChallengeInteraction

# Register your models here.
admin.site.register(User)
admin.site.register(Challenge)
admin.site.register(Friendship)
admin.site.register(ChallengeInteraction)
