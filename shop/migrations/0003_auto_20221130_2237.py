# Generated by Django 2.2.8 on 2022-11-30 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20221129_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra_images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.Product', verbose_name='extra_image'),
        ),
    ]
