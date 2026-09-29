from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                'Invalid username or password'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This account is inactive'
            )

        refresh = RefreshToken.for_user(user)

        attrs['user'] = username
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):

        refresh_token = attrs['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise serializers.ValidationError(
                'Invalid or already blacklisted refresh token'
            )

        return attrs