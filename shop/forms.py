from django import forms
from .models import Product, category, extra_images

def set_field_html_name(cls, new_name):
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category','status','condition', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','style': 'height: 100px'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control' }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control' }),
        }
class ExtraImagesForm(forms.ModelForm):
    img = forms.FileField(required=False)
    class Meta:
        model = extra_images
        fields = ('img',)
        labels = {
            'img': 'Extra Images',
        }
    def save(self, commit=True):
        cleaned_data = super(ExtraImagesForm,self).clean()
        if 'img' in cleaned_data:
            img = cleaned_data['img']
            # check images uploaded are less than 5
            if len(img) > 5:
                self.add_error('img', 'You can upload a maximum of 5 images')
            # save the images
            for i in img:
                extra_images.objects.create(img=i)
        if commit:
            cleaned_data.save()
        return self.cleaned_data
    img.widget.attrs.update({'class': 'form-control', 'type': 'file', 'accept' :".png, .jpg, .jpeg" , 'multiple': 'multiple'})
                
    
