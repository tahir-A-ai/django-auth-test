from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_description="Register a new user.",
        responses={
            201: RegisterSerializer,
            400: "Bad Request (e.g. Email exists)"
        },
        tags=['Authentication'],
    )

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            return Response({
                'status': 200,
                'message': 'User registered successfully',
                'data': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'phone': user.phone,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)
        


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    @swagger_auto_schema(
        operation_description="Login a user.",
        responses={
            200: CustomTokenObtainPairSerializer,
            400: "Bad Request (e.g. Invalid credentials)"
        },
        tags=['Authentication'],
    )

    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomTokenObtainPairSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)
        

class MyProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    @swagger_auto_schema(
        operation_description="Get my profile.",
        security=[{'Bearer': []}],
        responses={
            200: UserSerializer,
            401: "Unauthorized",
            404: "Not Found"
        },
        tags=['Profile'],
    )

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'status': 200,
                'message': 'User profile retrieved successfully',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)


class EditProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    @swagger_auto_schema(
        operation_description="Edit my profile.",
        security=[{'Bearer': []}],
        responses={
            200: UserSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found"
        },
        tags=['Profile'],
    )

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'status': 200,
                'message': f'Profile updated successfully for user {instance.email}',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)
