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

class ExtraImagesForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': 'True'}))
    class Meta:
        model = extra_images
        fields = ('img',)
        labels = {
            'img': 'Extra Images',
        }
    img.label = 'Extra Images'
