from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from datetime import timedelta, datetime



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                lifetime_seconds = 3600  # Exp time is set as 1 hour
                lifetime = timedelta(seconds=lifetime_seconds)
                refresh.access_token.set_exp(lifetime=lifetime)
                return {
                    'username': user.username,
                    'email': user.email,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }
            else:
                raise serializers.ValidationError("Incorrect username or password!")
        else:
            raise serializers.ValidationError("Both username and password are required!")
        
