from django.core.cache import cache

from blog.models import Post
from config.settings import CACHE_ENABLED


def get_posts_from_cache():
    if not CACHE_ENABLED:
        return Post.objects.all()
    key = "posts_list"
    posts = cache.get(key)
    if posts is not None:
        return posts

    posts = Post.objects.all()
    cache.set(key, posts)
    return posts
