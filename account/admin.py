from django.contrib import admin
from .models import User, Interest, Follow

admin.site.register(User)
admin.site.register(Interest)

class AdminFollow(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')
    list_editable = ('follower', 'following')
    
admin.site.register(Follow, AdminFollow)