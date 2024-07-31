import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs['email']
        existing_email = User.objects.filter(email=email).first()
        if existing_email: # checking for uniqueness
            raise serializers.ValidationError(
                {
                    'detail': 'Email or password fields are incorrect.',
                    'message': ('Password must be at least 8 characters long, '
                              'contain at least one uppercase and one lowercase letter.')
                }
            )
        if not re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise serializers.ValidationError(
                {
                    'detail': 'Email or password fields are incorrect.',
                    'message': ('Password must be at least 8 characters long, '
                              'contain at least one uppercase and one lowercase letter.')
                }
            )
        password = attrs['password']
        if (not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password)) or len(password) < 8:
            raise serializers.ValidationError(
                {
                    'detail': 'Email or password fields are incorrect.',
                    'message': ('Password must be at least 8 characters long, '
                              'contain at least one uppercase and one lowercase letter.')
                }
            )
        return attrs        
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid login credentials")
    

class LogoutSerializer(serializers.Serializer):
    message = serializers.CharField()
