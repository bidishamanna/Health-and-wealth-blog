import re
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        fields = ['id', 'name', 'email', 'password']

        
        extra_kwargs = {        # This allows the password field to be included in requests but excluded from responses.
            'password': {'write_only': True}  #write_only=True: The password can be used in input , but it won’t be returned in API responses — for security.
        }
    
    # Custom validation for email ending with a specific domain
    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError("Only '@example.com' emails are allowed.")
        return value

    # # Custom field-level validation for username
    # def validate_username(self, value):
    #     if len(value) < 4:
    #         raise serializers.ValidationError("Username must be at least 4 characters long.")
    #     return value

    # Custom field-level validation for password
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value

    # Object-level validation (useful if validation depends on multiple fields)
    def validate(self, data):
        if data['name'] == " ":
            raise serializers.ValidationError("name cannot be empty.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) #This line dynamically creates a new instance of the model (User in this case) using the validated input data — except the password, which was removed just before this line.
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

