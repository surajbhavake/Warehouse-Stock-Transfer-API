from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        serializer = LoginSerializer(
            data = request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data['user']

        return Response(
            {
                'access' : serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'user':{
                    'id':user.id,
                    'username':user.username,
                    'email':user.email
                }
            },
            status=status.HTTP_200_OK
        )