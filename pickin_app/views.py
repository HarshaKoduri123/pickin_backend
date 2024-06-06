from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,SalesSerializer, InvoiceSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import InvoiceFile, SalesFile
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import csv
import os



def index(request):
    return render(request, 'index.html')


class UserRegister(APIView):
	permission_classes = (permissions.AllowAny,)
	def post(self, request):
		clean_data = custom_validation(request.data)
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
		
		return Response({'business_type':serializer.data['business_type'] }, status=status.HTTP_200_OK)


class InvoiceView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user = request.user
		invoice_files = InvoiceFile.objects.filter(user=user)
		serializer = InvoiceSerializer(invoice_files, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		serializer = InvoiceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)  # Pass user to the save method
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SalesView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user = request.user
		sales_files = SalesFile.objects.filter(user=user)
		serializer = SalesSerializer(sales_files, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		print(request.data)
		serializer = SalesSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user)  # Pass user to the save method
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductsView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user = request.user
		base_dir = settings.BASE_DIR
		file_path = os.path.join(base_dir, 'user_files', 'Products.xlsx')

		if not os.path.exists(file_path):
			return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

		df = pd.read_excel(file_path, nrows=10)  
		first_10_rows = df.head(10)

		response_data = first_10_rows.to_json(orient="records")
		
		return HttpResponse(response_data, content_type="application/json")

	def post(self, request):
		user = request.user
		base_dir = settings.BASE_DIR
		file_path = os.path.join(base_dir, 'user_files', 'Products.xlsx')

		if not os.path.exists(file_path):
			return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

		query = request.data.get('query', '')
		category = request.data.get('category', '')

		if not query or not category:
			return Response({"error": "Query and category are required."}, status=status.HTTP_400_BAD_REQUEST)

		df = pd.read_excel(file_path)

		if category == 'Item ID':
			column = 'ItemID'
		elif category == 'Item Name':
			column = 'Description'
		else:
			return Response({"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST)

		# Filter the DataFrame
		filtered_rows = df[df[column].astype(str).str.contains(query, case=False, na=False)]
		print(query, category, filtered_rows)

		if filtered_rows.empty:
			return Response({"error": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)

		response_data = filtered_rows.to_json(orient="records")
		return HttpResponse(response_data, content_type="application/json")
	
class MessageView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)

	def get(self, request):
		user_id = request.user
		file_path = os.path.join(settings.BASE_DIR, 'user_files', f'{request.user.user_id}.csv')
		if not os.path.exists(file_path):
			
			return Response({"message": []}, status=status.HTTP_200_OK)
		
		messages = []
		with open(file_path, 'r') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				
				messages.append({"sender": row[0], "text": row[1]})

		return Response({"message": messages}, status=status.HTTP_200_OK)

	def post(self, request):
		

		message = request.data.get('message')
		

		if not message:
			return Response({"error": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

		file_path = os.path.join(settings.BASE_DIR, 'user_files', f'{request.user.user_id}.csv')
		

		file_exists = os.path.isfile(file_path)

		with open(file_path, 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			# Write the data row
			writer.writerow(['user', message])
			writer.writerow(['admin', "Thanks for contacting, we will look into it"])



		# # Read existing data and append new message if user_id is found
		# if os.path.exists(file_path):
		# 	with open(file_path, 'r', newline='') as csvfile:
		# 		reader = csv.reader(csvfile)
		# 		for row in reader:
		# 			if row[0] == user_id:
		# 				row[1] = row[1] + " " + message
		# 				user_found = True
		# 			new_rows.append(row)
		# 			new_rows.append(['admin', "we will get back soon"])

		# # If user_id is not found, add a new row
		# if not user_found:
		# 	new_rows.append([user_id, message])
		# 	new_rows.append(['admin', "we will get back soon"])

		# # Write updated data back to the CSV file
		# with open(file_path, 'w', newline='') as csvfile:
		# 	writer = csv.writer(csvfile)
		# 	writer.writerows(new_rows)

		return Response({"message": "Message saved successfully."}, status=status.HTTP_200_OK)

	