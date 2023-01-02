# check if the user is the owner of the product
if request.user.id == product.owner_id:
    return JsonResponse({'success': True})
return JsonResponse({'success': False})
context = {
    'product': product,
    'form': form,
    'form2': form2
}
return render(request, 'product-edit.html', context)