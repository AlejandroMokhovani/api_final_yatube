from django.contrib import admin

from .models import Post, Comment, Follow, Group

class PostAdmin(admin.ModelAdmin):
    """Posts в админке."""
    list_display = ('author', 'text', 'pub_date', 'group',)
    list_display_links = ('author',)
    list_filter = ('author',)
    search_fields = ('author',)
    empty_value_display = '-пусто-'

class CommentAdmin(admin.ModelAdmin):
    """Comments в админке."""
    list_display = ('author', 'post', 'text', 'created',)
    list_display_links = ('author',)
    list_filter = ('author',)
    search_fields = ('author',)
    empty_value_display = '-пусто-'

class FollowAdmin(admin.ModelAdmin):
    """Follows в админке."""
    list_display = ('user', 'following',)
    list_display_links = ('user',)
    list_filter = ('user', 'following',)
    search_fields = ('author',)
    empty_value_display = '-пусто-'

class GroupAdmin(admin.ModelAdmin):
    """Follows в админке."""
    list_display = ('title', 'slug', 'description',)
    list_display_links = ('slug',)
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Group, GroupAdmin)
