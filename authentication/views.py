from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer,LogoutSerializer
from inventory.throttles import LoginRateThrottle

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    throttle_classes = [LoginRateThrottle]

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

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {'message':'Logout Successfly'},
            status=status.HTTP_200_OK
        )