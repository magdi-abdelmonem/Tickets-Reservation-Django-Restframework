from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields=['hall','movie']


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields=['pk','reservation','name','mobile']


class reservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'