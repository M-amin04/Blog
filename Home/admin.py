from django.contrib import admin
from . import models
from .models import Profile, ContactMessage


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ['title']

admin.site.register(models.Category)
admin.site.register(Profile)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created')
    list_filter = ('subject', 'created')
    search_fields = ['name', 'email', 'message']