from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        attrs['user'] = user
        return attrs
