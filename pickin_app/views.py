from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserInvoiceSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import UserFile
from django.core.mail import send_mail
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
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
		serializer = UserInvoiceSerializer(user_files, many=True)
		print(serializer.data)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = UserInvoiceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)  # Pass user to the save method
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		print(serializer.errors)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReadExcelView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	def get(self, request):
		user = request.user

		user_files = UserFile.objects.filter(user=user)
		if not user_files:
			return Response({"error": "No files uploaded by the user."}, status=status.HTTP_404_NOT_FOUND)

		# Assuming the user has only one file. Modify if multiple files are expected.
		file_obj = user_files.first()

		file_path = file_obj.file.path  # Get the file path
		file_path = os.path.dirname(file_path)+"/Products.xlsx"

		if not os.path.exists(file_path):
			return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

		df = pd.read_excel(file_path)  # Read the Excel file into a DataFrame
		first_10_rows = df.head(10)  # Get the first 10 rows

		# Convert the DataFrame to JSON for response
		response_data = first_10_rows.to_json(orient="records")
		print(response_data)

		return HttpResponse(response_data, content_type="application/json")
