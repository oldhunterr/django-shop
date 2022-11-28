from tempfile import NamedTemporaryFile
from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
import requests
from django.core.files import File
from urllib.request import urlopen
# allauth user-signup signal
@receiver(user_logged_in)
def pre_social_login(request, user, **kwargs):
    
    # get the profile where i want to store the extra_data
    profile = user
    print(type(profile))
    # in this signal I can retrieve the obj from SocialAccount
    data = SocialAccount.objects.filter(user=user, provider='google')
    # check if the user has signed up via social media
    if data:
        picture = data[0].get_avatar_url()
        # profile.get_image_from_url(picture)
        profile.get_image_from_url(picture)
        profile.name = data[0].extra_data['name']
        profile.save()

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', default='avatars/avatar.png')
    avatar_url = models.URLField(null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
        
    # download the image from the url and save it to the model default storage
    def get_image_from_url(self, url):
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        # print(self.avatar_url)
        # print(url)
        if self.avatar_url == url:
          if self.avatar:
            return
          else:
            # delete image from default storage
            self.avatar.delete()
            self.avatar.save(f"{self.email}.jpg", File(img_temp))
        else:
          self.avatar_url = url
          # delete image from default storage
          self.avatar.delete()
          self.avatar.save(f"{self.email}.jpg", File(img_temp))
