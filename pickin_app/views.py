from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserFileSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import UserFile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import os


def index(request):
    return render(request, 'index.html')


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
		print(clean_data)
		serializer = UserRegisterSerializer(data=clean_data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.create(clean_data)
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = (SessionAuthentication,)
	##
	def post(self, request):

		data = request.data
		assert validate_email(data)
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class BusinessTypeView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user = request.user
		serializer = UserSerializer(request.user)
		print(serializer.data)
		
		return Response({'business_type':serializer.data['business_type'] }, status=status.HTTP_200_OK)


class UserFileUploadView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user = request.user

		user_files = UserFile.objects.filter(user=user)
		serializer = UserFileSerializer(user_files, many=True)
		print(serializer.data)
		return Response(serializer.data)
	
	def post(self, request):
		print(request.data)
		serializer = UserFileSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)  # Pass user to the save method
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)