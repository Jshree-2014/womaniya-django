"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('jshree/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='product_by_category'), #path for item by category,from here the name is passed to category models get_url fuction to return url of categories
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),#path for each product details
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

]
