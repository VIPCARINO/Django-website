from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    description = models.TextField()

    # software-specific fields
    tech_stack = models.CharField(max_length=255, blank=True)  # Django, PyTorch, etc
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    demo_video = models.URLField(blank=True)

    # classification
    category = models.ForeignKey("ProductCategory", on_delete=models.SET_NULL, null=True, blank=True)

    # monetization (optional future)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):

        return reverse(
            "products:product_detail",
            kwargs={
                "slug": self.slug
            }
        )

    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="product_gallery/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.title} image"
    
from django.contrib.auth.models import User

class ProductLike(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user} likes {self.product.title}"
    
class ProductRating(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField()  # 1 to 5

    class Meta:
        unique_together = ("product", "user")