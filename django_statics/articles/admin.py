from django.contrib import admin
from .models import Article

# Register your models here.
class Admin2(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'image', 'created_at', 'updated_at')

admin.site.register(Article, Admin2)