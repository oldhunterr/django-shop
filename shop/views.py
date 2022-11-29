from django.shortcuts import render
from shop.models import Product
from shop.models import category
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.
def search(request):
    print(request)
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        categ = json.loads(request.body).get('category')
        # print(search_text)
    else:
        search_text = ''
    if categ:
        print(categ)
        products = Product.objects.filter(name__icontains=search_text, category=categ) | Product.objects.filter(description__icontains=search_text, category=categ)
    else:
        products = Product.objects.filter(name__icontains=search_text) | Product.objects.filter(description__icontains=search_text)
    data = products.values()
    for product in data:
        product['category'] = category.objects.get(id=product['category_id']).name
    # return render(request, 'ajax_search.html', {'products': products})
    return JsonResponse(list(data), safe=False)
def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 20)
    categories = category.objects.filter(parent=None)
    page = paginator.get_page(request.GET.get('page'))
    context = {
        'page': page,
        'products': products,
        'categories': categories
        }

    # get categories without parents
    return render(request, 'home.html', context)