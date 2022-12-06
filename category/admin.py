from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin): #to auto populate the category name in slug,its admin bcoz only admin can push data
    prepopulated_fields = {'slug': ('category_name',)}  #to prepopulate the categor name is slug
    list_display = ('category_name', 'slug')  #it displays thing on table in database

# Register your models here.
admin.site.register(Category,CategoryAdmin)