from django.shortcuts import render
from shop.models import Product
from shop.models import category
import json
from django.http import JsonResponse
# Create your views here.
def search(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
    else:
        search_text = ''
    products = Product.objects.filter(name__icontains=search_text) | Product.objects.filter(description__icontains=search_text)
    data = products.values()
    # return render(request, 'ajax_search.html', {'products': products})
    return JsonResponse(list(data), safe=False)

def home(request):
    products = Product.objects.all()
    # get categories without parents
    categories = category.objects.filter(parent=None)
    return render(request, 'home.html', {'products': products, 'categories': categories})