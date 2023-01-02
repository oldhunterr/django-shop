from django.shortcuts import redirect, render
from django.db.models import Q
from shop.models import Product
from shop.models import category
from shop.models import extra_images
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import *
from metadata.models import product_status
from django.contrib import messages
from django.utils.encoding import force_text
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


# Create your views here.
# def search(request):
#     print(request)
#     if request.method == 'POST':
#         search_text = json.loads(request.body).get('searchText')
#         categ = json.loads(request.body).get('category')
#         # print(search_text)
#     else:
#         search_text = ''
#     if categ:
#         print(categ)
#         products = Product.objects.filter(name__icontains=search_text, category=categ) | Product.objects.filter(description__icontains=search_text, category=categ)
#     else:
#         products = Product.objects.filter(name__icontains=search_text) | Product.objects.filter(description__icontains=search_text)
#     data = products.values()
#     for product in data:
#         product['category'] = category.objects.get(id=product['category_id']).name
#     # return render(request, 'ajax_search.html', {'products': products})
#     return JsonResponse(list(data), safe=False)

# def search(request):
#     if request.method == 'POST':
#         search_text = json.loads(request.body).get('searchText')
#         categ = json.loads(request.body).get('category')
#         sort = json.loads(request.body).get('sort')
#     else:
#         search_text = ''

#     # Use the Q objects to combine the two filters into a single filter
#     # Use the __icontains lookup to perform a case-insensitive search
#     from django.db.models import Q
#     query = Q(name__icontains=search_text) | Q(description__icontains=search_text)

#     if categ:
#         # Filter by category if provided
#         products = Product.objects.filter(query, category=categ)
#     else:
#         products = Product.objects.filter(query)

#     if sort == 'date_desc':
#         products = products.order_by('-created_at')
#     if sort == 'date_asc':
#         print(products)
#         # Sort by date (oldest first)
#         products = products.order_by('created_at')
#         print(products)
#     elif sort == 'price_asc':
#         # Sort by price (lowest first)
#         products = products.order_by('price')
#     elif sort == 'price_desc':
#         # Sort by price (highest first)
#         products = products.order_by('-price')

#     # Retrieve only the necessary fields to reduce the amount of data transferred
#     data = products.values('id', 'name', 'description', 'category_id', 'price', 'image', 'created_at')

#     # Add the category name to the data for each product
#     for product in data:
#         product['category'] = category.objects.get(id=product['category_id']).name

#     #     # return render(request, 'ajax_search.html', {'products': products})
#     return JsonResponse(list(data), safe=False)

def search(request):
    if request.method == 'POST':
        search_text = json.loads(request.body).get('searchText')
        categ = json.loads(request.body).get('category')
        sort = json.loads(request.body).get('sort')
        print('Search: '+search_text, 'Category: '+categ, 'Sort: '+sort)
    else:
        search_text = ''
        categ = None
        sort = None
    # Use the Q objects to combine the two filters into a single filter
    # Use the __icontains lookup to perform a case-insensitive search
    from django.db.models import Q
    query = Q(name__icontains=search_text) | Q(description__icontains=search_text)

    if categ:
        # Filter by category if provided
        products = Product.objects.filter(query, category=categ)
    else:
        products = Product.objects.filter(query)
    products =  products.filter(status_id=1)
    if sort == 'price_asc':
        # Sort by price (lowest first)
        products = products.order_by('price')
    elif sort == 'price_desc':
        # Sort by price (highest first)
        products = products.order_by('-price')
    # Retrieve only the necessary fields to reduce the amount of data transferred
    data = products.values('id', 'name', 'description', 'category_id', 'price', 'image', 'created_at')

    # Add the category name to the data for each product
    for product in data:
        product['category'] = category.objects.get(id=product['category_id']).name
    print('Data: '+str(data))
    #     # return render(request, 'ajax_search.html', {'products': products})
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
    # get status id of active fron product_status table
    status = product_status.objects.get(name='Active')
    products = products.filter(status_id=status.id)
    products = products.order_by('-created_at')
    paginator = Paginator(products, 5)
    categories = category.objects.filter(parent=None)
    page = paginator.get_page(request.GET.get('page'))
    context = {
        'page': page,
        'products': products,
        'categories': categories
        }

    # get categories without parents
    return render(request, 'home.html', context)

@login_required
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
    # check if product is active
    if product.status_id != 1:
        raise PermissionDenied('This product is not active')
    extra_images = product.images.all()
    context = {
        'product': product,
        'extra_images': extra_images
    }
    return render(request, 'product_view.html', context)

# def edit(request, id):
#     product = Product.objects.get(id=id)
#     if product.owner_id != request.user.id:
#         # raise forbidden
#         raise PermissionDenied('You are not allowed to edit this product')
#     form = ProductForm(initial={'name': product.name, 'description': product.description, 'price': product.price, 'category': product.category, 'status': product.status, 'condition': product.condition})
#     form2 = ExtraImagesForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         form2 = ExtraImagesForm(request.POST, request.FILES)
#         print(request.FILES)
#         if form.is_valid() and form2.is_valid():
#             deleted_images = request.POST.getlist('checkbox')
#             if deleted_images:
#                 for image in deleted_images:
#                     img = extra_images.objects.get(id=image)
#                     if img.img:
#                         img.img.delete()
#                     img.delete()
#             for img in request.FILES.getlist('img'):
#                 extra_images.objects.create(img=img, product=product)
#             # update product
#             product.name = form.cleaned_data['name']
#             product.description = form.cleaned_data['description']
#             product.price = form.cleaned_data['price']
#             product.category = form.cleaned_data['category']
#             product.status = form.cleaned_data['status']
#             product.condition = form.cleaned_data['condition']
#             if request.FILES.get('image'):
#                 # delete old image
#                 print('yes i have image')
#                 product.image.delete()
#                 product.image = request.FILES.get('image')
#             product.save()
#             # redirect back to product view
#             messages.success(request, 'Form submission successful')
#             return redirect('edit', id=product.id)

#     context = {'product': product, 'form': form, 'form2': form2}
#     return render(request, 'product-edit.html', context)

@login_required
def edit(request, id):
    # Get the product or raise a 404 error if it does not exist
    product = get_object_or_404(Product, id=id)
    # Check if the user is the owner of the product
    if product.owner_id != request.user.id:
        raise PermissionDenied('You are not allowed to edit this product')
    # Create the forms with the initial data from the product
    form = ProductForm(initial={'name': product.name, 'description': product.description, 'price': product.price, 'category': product.category, 'status': product.status, 'condition': product.condition})
    form2 = ExtraImagesForm()
    if request.method == 'POST':
        # Bind the form data to the forms
        form = ProductForm(request.POST, request.FILES)
        form2 = ExtraImagesForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            # Delete the selected extra images
            deleted_images = request.POST.getlist('checkbox')
            if deleted_images:
                extra_images.objects.filter(id__in=deleted_images).delete()
            # Create the extra images
            extra_images_data = [extra_images(img=img, product=product) for img in request.FILES.getlist('img')]
            extra_images.objects.bulk_create(extra_images_data)
            # Update the product
            # Product.objects.filter(id=product.id).update(**form.cleaned_data)
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
            # Redirect back to
            messages.success(request, 'Form submission successful')
            return redirect('edit', id=product.id)

    context = {'product': product, 'form': form, 'form2': form2}
    return render(request, 'product-edit.html', context)

@login_required
def delete(request, id):
    product = Product.objects.get(id=id)
    if product.owner_id != request.user.id:
    # raise forbidden
        raise PermissionDenied('You are not allowed to Delete this product')
    # delete product and extra images
    extra = extra_images.objects.filter(product_id=id)
    for img in extra:
        img.img.delete()
    name = product.name
    product.image.delete()
    product.delete()
    messages.success(request, 'Product '+name+' deleted successfully')
    return redirect('profile')
