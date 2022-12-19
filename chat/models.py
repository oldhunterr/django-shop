from django.contrib.auth import get_user_model
from django.db import models
from shop.models import Product
from django.template.defaultfilters import slugify

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey('Room', related_name='room_messages', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.author.name
    # get the last 10 messages
    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    member1 = models.ForeignKey(User, related_name='member1', on_delete=models.CASCADE)
    member2 = models.ForeignKey(User, related_name='member2', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    # check if the user is in the room
    def check_user(self, user):
        if user == self.member1 or user == self.member2:
            return True
        return False
    # get the second user in the room
    def get_second_user(self, user):
        if user == self.member1:
            return self.member2
        return self.member1
    # save to change the slug
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify("chat-"+self.member1.name +"-"+ self.member2.name+"-"+self.product.name)
        super(Room, self).save(*args, **kwargs)
    