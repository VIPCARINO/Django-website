from django.db import models
from django.urls import reverse

# Create your models here.

class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)

    who_i_am = models.TextField()

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Journey(models.Model):
    text = models.TextField()