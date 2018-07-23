from hashlib import sha512
from rest_framework import serializers
from fourthwatch.auth_core import models
from django.contrib.auth.hashers import check_password

class UserRegistrationSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()
	first_name = serializers.CharField()

	def create(self, validated_data):
		email = self.validated_data['email']
		self.validated_data['username'] = email
		user = models.Users(**self.validated_data)
		has_rec = models.Users.objects.filter(username= email)
		if has_rec.count() > 0:
			return has_rec.count() , False
		user.save()
		return user ,True

	class Meta:
		model = models.Users
		fields = ('email', 'password', 'first_name', 'last_name','user_type')



class BankRegistrationSerializer(serializers.ModelSerializer):
	user = UserRegistrationSerializer()
	class Meta:
		model = models.Bank
		fields = '__all__'

class BankEmployeeRegistrationSerializer(serializers.ModelSerializer):
	user = UserRegistrationSerializer()
	class Meta:
		model = models.BankEmployee
		fields = '__all__'

class CustomerRegistrationSerializer(serializers.ModelSerializer):
	user = UserRegistrationSerializer()
	class Meta:
		model = models.Customer
		fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(max_length=1000)

	def authenticate_create_token(self):
		# password = sha512(self.validated_data['password']).hexdigest()
		password = self.validated_data['password']
		user = models.Users.objects.filter(email=self.validated_data['email'])
		result = dict()
		if user.count() >= 1:
			user = user.get()
			pass_status = check_password(password, user.password)
			if pass_status:
				token = models.Token(user=user).save()
				result['status'] = True
				result['token'] = token.key
				return result
			else:
				result['status'] = False
				result['error'] = "Invalid Credentials"
				return result
		else:
			result['status'] = False
			result['error'] = "Invalid Credentials"
			return result

class VerifyOTPSerializer(serializers.Serializer):
	verification_code = serializers.CharField(min_length=6)
	email = serializers.EmailField()
	class Meta:
		fields = ('verification_code' , 'email')

class GetOTPSerializer(serializers.Serializer):
	email = serializers.EmailField()
	class Meta:
		model = models.Users
		fields =  ('email',)


class RequestForgetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()

	class Meta:
		fields = '__all__'

class ForgetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	key = serializers.CharField(max_length=40)
	new_password = serializers.CharField()

	class Meta:
		fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Users
		fields = ['first_name', 'last_name',  'username']
		read_only_fields = ['username']

