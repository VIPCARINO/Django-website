from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True
    )

    github_url = models.URLField(blank=True)

    live_url = models.URLField(blank=True)

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    youtube_url = models.URLField(blank=True, null=True)

    video = models.URLField(blank=True, null=True)

    def get_absolute_url(self):

        return reverse(
            "blogs:blog_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):
        return self.title
    
class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.blog.title}"
    
class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("blog", "user")

class BlogCode(models.Model):

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="snippets"
    )

    title = models.CharField(max_length=100)

    language = models.CharField(max_length=50)

    code = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.project.title}"