#it takes request as a argument and it will return the dictonary of data as a context
from .models import Category

def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)