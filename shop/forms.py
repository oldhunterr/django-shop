from django import forms
from .models import Product, category, extra_images

def set_field_html_name(cls, new_name):
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'image',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control','style': 'height: 100px'}),
            'price': forms.NumberInput(attrs={'class': 'form-control' }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control' }),
        }
class ExtraImagesForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': 'True', 'class': 'form-control'}))
    class Meta:
        model = extra_images
        fields = ('img',)
        labels = {
            'img': 'Extra Images',
        }
    img.label = 'Extra Images'
