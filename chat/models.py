import random
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
    # get the last 10 messages from room
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').filter(room=self)[:10]

class Room(models.Model):
    name = models.CharField(max_length=255, unique=False, null=True, blank=True, default='chat')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
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
    # get messages in the room
    def get_messages(self):
        return Message.objects.filter(room=self).order_by('-timestamp')
    # check if the slug is used
    def check_slug(self, slug):
        if Room.objects.filter(slug=slug).exists():
            if Room.objects.filter(slug=slug).first() == self:
                return False
            return True
        return False
    def check_name(self, name):
        if Room.objects.filter(name=name).exists():
            if Room.objects.filter(name=name).first() == self:
                return False
            return True
        return False
    # save to change the slug
    def save(self, *args, **kwargs):
        # check if slug is used
        print('slug', self.slug)
        if not self.slug or self.slug == None:
            self.slug = slugify("chat_"+self.member1.name +"_"+ self.member2.name+"_"+self.product.name)
            # relpace - with _ Because - is not allowed in url for websocket
            self.slug = self.slug.replace("-", "_")

        if self.check_slug(self.slug):
            # update slug
            self.slug = slugify(self.slug+"_"+str(random.randint(1000, 9999)))
        # check if name is used
        if self.check_name(self.name):
            # update name
            self.name = self.name+"_"+str(random.randint(1000, 9999))
        super(Room, self).save(*args, **kwargs)
        # check if both users are not the same
        if self.member1 == self.member2:
            raise ValueError("Both users can't be the same")