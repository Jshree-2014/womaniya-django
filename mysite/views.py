import imp
from multiprocessing import context
from django.shortcuts import HttpResponse
from django.shortcuts import render
from store.models import Product
from store.models import Product, ReviewRating
def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date') #get all those product which are avalilable 

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context={
        'products':products,
        'reviews': reviews,
    }


    return render(request,'home.html',context) # not possible to send template via HTTP response so we use render ,context so this above product will be on home page