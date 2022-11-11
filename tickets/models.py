from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Movie(models.Model):
    hall=models.CharField(max_length=50)
    movie=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.movie)

class Guest(models.Model):
    name=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

class Reservation(models.Model):
   guest=models.ForeignKey(Guest,related_name='reservation', on_delete=models.CASCADE) 
   movie=models.ForeignKey(Movie,related_name='reservation',on_delete=models.CASCADE)

   def __str__(self):
        return str(self.guest)



@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,instance,created,**wargs):
    if created :
        Token.objects.create(user=instance)