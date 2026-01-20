from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProfileImageSerializer, RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Wallet
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary.uploader
import os

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
            Wallet.objects.create(user=user, balance=0)
            
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



class UploadProfileImageView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileImageSerializer

    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user
    @swagger_auto_schema(
        operation_description="Upload profile image.",
        manual_parameters=[
            openapi.Parameter(
                'profile_image',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Profile image file'
            )
        ],
        responses={
            200: ProfileImageSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found"
        },
        tags=['Profile'],
    )

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            had_profile_image = bool(user.profile_image)
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user.refresh_from_db()

                local_file_path = user.profile_image.path
                if local_file_path and os.path.exists(local_file_path):
                    upload_response = cloudinary.uploader.upload(
                        local_file_path, 
                        folder="user_profiles"
                    )  

                user.cloudinary_url = upload_response.get('secure_url')
                user.cloudinary_public_id = upload_response.get('public_id')
                user.save()

                user_wallet, created = Wallet.objects.get_or_create(
                    user=user,
                    defaults={'balance': 0, 'currency': 'Gems'}
                )

                if not had_profile_image and user.profile_image:
                    reward_points = 3
                    user_wallet.balance += reward_points
                    user_wallet.save()

                return Response({
                    'status': 200,
                    'message': 'Profile image uploaded successfully',
                    "data": { 
                    "cloudinary_url": user.cloudinary_url
                }}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)


class DeleteProfileImageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
         operation_description="Delete profile image.",
         responses={
             200: "ok",
             400: "Bad Request",
             401: "Unauthorized",
             404: "Not Found"
         },
     )
    
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if not user.profile_image and not user.cloudinary_public_id:
             return Response({
                "status": "error",
                "message": "No profile image found to delete."
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            if user.cloudinary_public_id:
                cloudinary.uploader.destroy(user.cloudinary_public_id)
            if user.profile_image:
                local_path = user.profile_image.path
                if os.path.exists(local_path):
                    os.remove(local_path)

            user.profile_image = None
            user.cloudinary_url = None
            user.cloudinary_public_id = None
            user.save()

            return Response({
                "status": "success",
                "message": "Profile image deleted from Cloud and Local storage."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error", 
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class EditProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    @swagger_auto_schema(
        operation_description="Edit my profile.",
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
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 400, 'message': str(e)
            }, status = status.HTTP_400_BAD_REQUEST)
