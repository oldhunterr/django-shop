# Generated by Django 2.2.8 on 2022-12-23 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/no_avatar.jpg', null=True, upload_to='avatars/'),
        ),
    ]
