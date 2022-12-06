from distutils.command.upload import upload
from unicodedata import category
from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=100,unique=True) #slugfield bcoz it will copy the category name
    description=models.CharField(max_length=255,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)

    class Meta: #in database we can see that the model name appears to be plural that is with extra 's' in end to make it singular we have written this meta class
        verbose_name='category' #name of model
        verbose_name_plural='categories' # singlural name of model

    def get_url(self):
        return reverse('product_by_category', args=[self.slug]) #this will give the url for every category in category bar

# Create your models here.
    def __str__(self):
        return self.category_name  #this will show the name of category in database 
