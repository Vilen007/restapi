from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        fields = ['username', 'password']

class AddBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'