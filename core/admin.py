from django.contrib import admin

# Register your models here.
from .models import AboutPage, Skill, Journey

admin.site.register(AboutPage)
admin.site.register(Skill)
admin.site.register(Journey)