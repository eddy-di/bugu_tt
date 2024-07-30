from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema

from accounts.models import User
from accounts.serializers import LoginSerializer, LogoutSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "message": "User registered successfully."
            }, 
            status=status.HTTP_201_CREATED
        )
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response(
            {
                "user": RegisterSerializer(user).data,
                "message": "User logged in successfully."
            }, 
            status=status.HTTP_200_OK
        )
    

class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=None,
        responses=LogoutSerializer
    )
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(
            {
                'message': 'Logged out successfully.'
            },
            status=status.HTTP_200_OK
        )
