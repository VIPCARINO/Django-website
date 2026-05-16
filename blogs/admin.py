from django.contrib import admin
from .models import Blog, BlogCategory, BlogComment, BlogLike
from django.utils.text import slugify

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)

admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(BlogComment)
admin.site.register(BlogLike)