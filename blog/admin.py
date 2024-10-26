# blog/admin.py

from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'views')
    search_fields = ('title',)
    readonly_fields = ('views', 'published_at')
    list_filter = ('published_at',)
    ordering = ('-published_at',)
