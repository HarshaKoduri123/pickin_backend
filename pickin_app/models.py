from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
	def create_user(self, fullname, business_name, business_type, address, city, state, zip_code, phone, contact_person, email, website, comments,  password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)

		user = self.model(
					email=email,
					fullname=fullname,
					business_name=business_name,
					business_type=business_type,
					address=address,
					city=city,
					state=state,
					zip_code=zip_code,
					phone=phone,
					contact_person=contact_person,
					website=website,
					comments=comments,
					password=password
				)

		user.set_password(password)
		user.save()
		return user
	
	def create_superuser(self, username, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.save(using=self._db)
		return user



class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	fullname = models.CharField(max_length=100)
	business_name = models.CharField(max_length=100, blank=True)
	business_type = models.CharField(max_length=100, blank=True)
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	contact_person = models.CharField(max_length=100, blank=True)
	website = models.URLField(blank=True)
	comments = models.TextField(blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['fullname', 'business_name', 'business_type', 'address', 'city', 'state', 'zip_code', 'phone', 'contact_person']

	objects = AppUserManager()
	def __str__(self):
		return self.fullname

class UserFile(models.Model):
	user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
	file = models.FileField(upload_to='user_files/')
	invoice_no = models.CharField(max_length=50, default='Null')
	distributor_name = models.CharField(max_length=100, default='Null')
	invoice_date = models.DateField()
	remarks = models.TextField(blank=True, null=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)