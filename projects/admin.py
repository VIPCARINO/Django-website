from django.contrib import admin
from .models import Project, ProjectCategory, ProjectComment, ProjectLike, ProjectCode
from django.utils.text import slugify

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title)
    super().save(*args, **kwargs)

admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(ProjectComment)
admin.site.register(ProjectLike)
admin.site.register(ProjectCode)