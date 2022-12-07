from email.errors import CloseBoundaryNotFoundDefect
from gc import get_objects
from .models import Product, ReviewRating,ProductGallery
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import OrderProduct

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug !=None: #this paginator is when user select particular category
        categories = get_object_or_404(Category, slug=category_slug) #if categories we search is not found it will return 404 error
        products = Product.objects.filter(category=categories,is_available=True) #to check if its available
        paginator = Paginator(products,1)
        page      = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else: #this paginator is when user clicks on all product
        products  = Product.objects.all().filter(is_available=True).order_by('id') #get all those product which are avalilable 
        paginator = Paginator(products,3) #out of available we took 3 one one page
        page      = request.GET.get('page') #here we capture url that comes with page number
        paged_products = paginator.get_page(page) #it will store the 3 item
        product_count = products.count()

    context={
        'products':paged_products, #we passing 3 item to template
        'counts':product_count,
    }

    return render(request,'store/store.html',context)
#__slug means accessing slug of that category item and will match with category_slug
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists() #if true it means product added into cart 
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET: #will get details of searched keyword
        keyword = request.GET['keyword'] #will get details of searched keyword and will store in keyword
        if keyword: #if keyword is not blank
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))#Q is working as OR operator to search keyword in descrption and name of items
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
# Create your views here.
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try: #if review already exist or not
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist: #if not then create new
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)