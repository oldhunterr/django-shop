from django.shortcuts import redirect, render
from shop.models import Product
from shop.models import category
from django.core.files.storage import FileSystemStorage
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages
from django.utils.encoding import force_text
from django.core.exceptions import PermissionDenied

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

def product_filter(request):
    if request.method == 'POST':
        status = json.loads(request.body).get('status')
        print(status)
        products = Product.objects.filter(status=status, owner=request.user)
        data = products.values()
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

def create(request):

    form = ProductForm()
    form2 = ExtraImagesForm()
    # form2.fields['extra_images'] = form2.fields['image']
    # get extra images widgets
    # form2['extra_images'].field.widget = form2['image'].field.widget
    # form2['extra_images'].field.label = form2['image'].field.label
    # del form2.fields['image']
    if request.method == 'POST':
        # print(request.POST)
        form = ProductForm(request.POST, request.FILES)
        form2 = ExtraImagesForm(request.POST, request.FILES)
        # print files
        print(request.FILES.getlist('img'))
        # check forms are valid
        if form.is_valid() and form2.is_valid():
            # save product
            product = form.save()
            product.owner_id = request.user.id
            product.save()
            print(product)
            # save extra images
            for img in request.FILES.getlist('img'):
                print(img)
                extra_images.objects.create(img=img, product=product)
            return JsonResponse({'success': True})
    context = { 'form': form , 'form2': form2 }
    return render(request, 'product-add.html', context)

def show(request, id):
    product = Product.objects.get(id=id)
    extra_images = product.images.all()
    print(extra_images)
    context = {
        'product': product,
        'extra_images': extra_images
    }
    return render(request, 'product_view.html', context)

def edit(request, id):
    product = Product.objects.get(id=id)
    if product.owner_id != request.user.id:
        # raise forbidden
        raise PermissionDenied('You are not allowed to edit this product')
    form = ProductForm(initial={'name': product.name, 'description': product.description, 'price': product.price, 'category': product.category, 'status': product.status, 'condition': product.condition})
    form2 = ExtraImagesForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form2 = ExtraImagesForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid() and form2.is_valid():
            deleted_images = request.POST.getlist('checkbox')
            if deleted_images:
                for image in deleted_images:
                    img = extra_images.objects.get(id=image)
                    if img.img:
                        img.img.delete()
                    img.delete()
            for img in request.FILES.getlist('img'):
                extra_images.objects.create(img=img, product=product)
            # update product
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.price = form.cleaned_data['price']
            product.category = form.cleaned_data['category']
            product.status = form.cleaned_data['status']
            product.condition = form.cleaned_data['condition']
            if request.FILES.get('image'):
                # delete old image
                print('yes i have image')
                product.image.delete()
                product.image = request.FILES.get('image')
            product.save()
            # redirect back to product view
            messages.success(request, 'Form submission successful')
            return redirect('edit', id=product.id)

    context = {'product': product, 'form': form, 'form2': form2}
    return render(request, 'product-edit.html', context)
def delete(request, id):
    # delete product and extra images
    extra = extra_images.objects.filter(product_id=id)
    for img in extra:
        img.img.delete()
    product = Product.objects.get(id=id)
    name = product.name
    product.image.delete()
    product.delete()
    messages.success(request, 'Product '+name+' deleted successfully')
    return redirect('profile')
