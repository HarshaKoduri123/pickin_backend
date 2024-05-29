from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import InvoiceFile, SalesFile
UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password', 'fullname', 'business_name', 'business_type', 'address', 'city', 'state', 'zip_code', 'phone', 'contact_person', 'website', 'comments']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],

            fullname=validated_data.get('fullname'),
            business_name=validated_data.get('business_name'),
            business_type=validated_data.get('business_type'),
            address=validated_data.get('address'),
            city=validated_data.get('city'),
            state=validated_data.get('state'),
            zip_code=validated_data.get('zip_code'),
            phone=validated_data.get('phone'),
            contact_person=validated_data.get('contact_person'),
            website=validated_data.get('website'),
            comments=validated_data.get('comments')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'fullname', 'business_name','business_type', 'phone')
		
class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = InvoiceFile
        fields = ['user', 'invoice_no', 'distributor_name', 'invoice_date', 'remarks', 'file']

class SalesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = SalesFile
        fields = ['user', 'period', 'to_date', 'from_date', 'remarks', 'file']