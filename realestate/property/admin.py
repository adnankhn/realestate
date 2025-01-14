from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Property)
class Property(admin.ModelAdmin):
    list_display = ('user','city')

@admin.register(models.PropertyImage)
class PropertyImage(admin.ModelAdmin):
    list_display = ('property','image') 

@admin.register(models.Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    list_display = ('user',)  