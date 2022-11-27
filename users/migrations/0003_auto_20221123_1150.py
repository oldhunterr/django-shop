# Generated by Django 2.2.8 on 2022-11-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/avatar.png', null=True, upload_to='avatars/'),
        ),
    ]