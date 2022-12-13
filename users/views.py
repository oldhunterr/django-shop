from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
from .forms import *
from metadata.models import *

# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        # get user
        form = ProfileForm(initial={'name': request.user.name})
        status = product_status.objects.all()
        data = SocialAccount.objects.filter(user=request.user, provider='google')
        # if data:
        #     form.fields['password1'].widget.attrs['disabled'] = True
        #     form.fields['password2'].widget.attrs['disabled'] = True
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                print('form is valid')
                print(form.cleaned_data)
                user = request.user
                user.name = form.cleaned_data['name']
                user.avatar = form.cleaned_data['avatar']
                if form.cleaned_data['password1'] and form.cleaned_data['password2']:
                    user.set_password(form.cleaned_data['password1'])
                user.save()
                update_session_auth_hash(request, user)
                # if form.cleaned_data['password1']:
                #     user.password = form.cleaned_data['password1']
                # user.save()
                return redirect('profile')
            else:
                print(form.errors)
        context = {'form': form, 'status': status, 'data': data}
        return render(request, 'profile.html', context)
