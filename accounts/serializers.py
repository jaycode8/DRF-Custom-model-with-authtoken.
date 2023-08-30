
from django.contrib.auth.models import make_password
from rest_framework import serializers
from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Users
        fields = '__all__'

    #def create(self, validated_data):
    #    password = validated_data.pop('password')
    #    hashed_password = make_password(password)
    #    instance = super().create(validated_data)
    #    instance.password = hashed_password
    #    instance.save()
    #    return instance
