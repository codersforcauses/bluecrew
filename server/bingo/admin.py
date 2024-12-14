from django.contrib import admin
from .models import User, Challenge, Friendship

# Register your models here.
admin.site.register(User)
admin.site.register(Challenge)
admin.site.register(Friendship)
