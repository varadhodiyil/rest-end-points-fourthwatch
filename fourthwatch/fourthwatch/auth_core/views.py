# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from hashlib import sha1

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response

from fourthwatch.auth_core import models, resources, serializers , class_model

# Create your views here.


class BankRegistration(GenericAPIView):
	""" Bank Registration """
	serializer_class = serializers.BankRegistrationSerializer
	parser_classes = (JSONParser, FormParser)

	def post(self, request, *args, **kwargs):
		data = request.data
		s = self.get_serializer(data=data)
		result = dict()
		if s.is_valid():
			user = s.validated_data['user']
			s.validated_data.pop('user')
			instance = s.save()
			user['user_type'] = instance

			user_s = serializers.UserRegistrationSerializer(data = user)
			if user_s.is_valid():
				user_s.validated_data['username'] = user_s.validated_data['email']
				business_emp = models.BankEmployee(bank=instance,is_admin=True)
				business_emp.save()
				user_s.validated_data['user_type'] = business_emp

				has_rec = models.Users.objects.filter(username= user_s.validated_data['email'])
				if has_rec.count() > 0:
					instance.delete()
					business_emp.delete()
					result['status'] = True
					result['error'] = "Account with Email already Exists!"
					return Response(result,status=status.HTTP_400_BAD_REQUEST)
				user_instance = models.Users(**user_s.validated_data)
				user_instance.set_password(user_instance.password)
				user_instance.save()
				result['status'] = True
				result['result'] = class_model.Bank().create(instance.id , instance.name)
				return Response(result,status=status.HTTP_201_CREATED)
			else:
				instance.delete()
				business_emp.delete()
				result['status'] = False
				result['errors'] = user_s.errors
				return Response(result,status=status.HTTP_200_OK)
		else:
			result['status'] = False
			result['errors'] = s.errors
			return Response(result,status=status.HTTP_200_OK)

	def get(self,request,*args,**kwargs):
		result = dict()
		result['status'] = True
		result['result'] = class_model.Bank().get()
		return Response(result,status=status.HTTP_201_CREATED)



class BankEmployeeRegistration(GenericAPIView):
	""" Bank Registration """
	serializer_class = serializers.BankEmployeeRegistrationSerializer
	parser_classes = (JSONParser, FormParser)

	def post(self, request, *args, **kwargs):
		data = request.data
		s = self.get_serializer(data=data)
		result = dict()
		if s.is_valid():
			user = s.validated_data['user']
			s.validated_data.pop('user')
			business_emp = s.save()
			user['user_type'] = business_emp

			user_s = serializers.UserRegistrationSerializer(data = user)
			if user_s.is_valid():
				user_s.validated_data['username'] = user_s.validated_data['email']
				
				user_s.validated_data['user_type'] = business_emp

				has_rec = models.Users.objects.filter(username= user_s.validated_data['email'])
				if has_rec.count() > 0:
					#instance.delete()
					business_emp.delete()
					result['status'] = True
					result['error'] = "Account with Email already Exists!"
					return Response(result,status=status.HTTP_400_BAD_REQUEST)

				user_instance = models.Users(**user_s.validated_data)
				# instance.delete()
				# user_instance = user_s.save()
				user_instance.set_password(user_instance.password)
				user_instance.save()
				result['status'] = True
				result['result'] = class_model.BankEmployee().create(business_emp.bank.id , business_emp.id,\
							user_instance.first_name,user_instance.last_name)
				return Response(result,status=status.HTTP_201_CREATED)
			else:
				business_emp.delete()
				result['status'] = False
				result['errors'] = user_s.errors
				return Response(result,status=status.HTTP_200_OK)
		else:
			result['status'] = False
			result['errors'] = s.errors
			return Response(result,status=status.HTTP_200_OK)

	def get(self,request,*args,**kwargs):
		result = dict()
		result['status'] = True
		result['result'] = class_model.BankEmployee().get()
		return Response(result,status=status.HTTP_201_CREATED)

class UserRegistration(GenericAPIView):
	""" User Registration """
	serializer_class = serializers.CustomerRegistrationSerializer
	parser_classes = ((JSONParser,FormParser))

	def post(self,request,*args,**kwargs):
		data = request.data
		s = self.get_serializer(data=data)
		result = dict()
		if s.is_valid():
			user = s.validated_data['user']
			s.validated_data.pop('user')
			customer = s.save()
			user['user_type'] = customer
			
			user_s = serializers.UserRegistrationSerializer(data = user)
			if user_s.is_valid():
				user_s.validated_data['username'] = user_s.validated_data['email']
				
				user_s.validated_data['user_type'] = customer
				user_instance = models.Users(**user_s.validated_data)
				has_rec = models.Users.objects.filter(username= user_s.validated_data['email'])
				if has_rec.count() > 0:
					#instance.delete()
					customer.delete()
					result['status'] = True
					result['error'] = "Account with Email already Exists!"
					return Response(result,status=status.HTTP_400_BAD_REQUEST)

				user_instance.set_password(user_instance.password)
				user_instance.save()
				result['status'] = True
				result['result'] = class_model.Customer().create(customer.bank.id,customer.id,customer.company,\
							user_instance.first_name,user_instance.last_name)
				return Response(result,status=status.HTTP_201_CREATED)
			else:
				customer.delete()
				result['status'] = False
				result['errors'] = user_s.errors
				return Response(result,status=status.HTTP_200_OK)
		else:
			result['status'] = False
			result['errors'] = s.errors
			return Response(result,status=status.HTTP_200_OK)

	def get(self,request,*args,**kwargs):
		result = dict()
		result['status'] = True
		result['result'] = class_model.Customer().get()
		return Response(result,status=status.HTTP_201_CREATED)


class UserLogin(GenericAPIView):
	""" User Login """
	serializer_class = serializers.UserLoginSerializer
	parser_classes = (JSONParser, FormParser)

	def post(self, request, *args, **kwargs):
		s = serializers.UserLoginSerializer(data=request.data)
		result = dict()
		if s.is_valid():
			result = s.authenticate_create_token()
			return Response(result, status=status.HTTP_200_OK)
		else:
			result['status'] = False
			result['errors'] = s.errors
			return Response(result, status=status.HTTP_200_OK)

class Profile(GenericAPIView):
	""" Profile """
	serializer_class = serializers.ProfileSerializer

	def get(self, request, *args, **kwargs):
		data = serializers.ProfileSerializer(request.user).data
		result = dict()
		
		if request.user.is_authenticated():
			result['result'] = data
			result['status'] = True
			result['user_type'] = request.user.user_type.__str__()
		else:
			result['error'] = "Please Login to Continue"
			result['status'] = False
		return Response(result, status=status.HTTP_200_OK)




# class VerifyOTP(GenericAPIView):
# 	serializer_class =  serializers.VerifyOTPSerializer
# 	parser_classes = ((JSONParser,FormParser))


# 	def post(self,request,*args,**kwargs):
# 		data = request.data
# 		result , status = resources.verify_otp(data)
# 		return  Response(result,status=status)

# class GetOTP(GenericAPIView):
# 	""" Dummy OTP module to be removed when we can afford sms gateway"""
# 	serializer_class =  serializers.GetOTPSerializer
# 	parser_classes = ((JSONParser,FormParser))


# 	def post(self,request,*args,**kwargs):
# 		data = request.data
# 		result , status = resources.get_otp(data)
# 		return  Response(result,status=status)


# class RequestForgotPassword(GenericAPIView):

#     serializer_class = serializers.RequestForgetPasswordSerializer
#     parser_classes = ((JSONParser,))

#     def post(self,request,*args,**kwargs):
#         data = request.data
#         s = serializers.RequestForgetPasswordSerializer(data=data)
#         result = dict()
#         if s.is_valid():
#             email = s.validated_data['email']
#             user = models.Users.objects.filter(email=email)
#             user = get_object_or_404(user)
#             _now = timezone.now()
#             _code_meta =  user.email + _now.strftime("%s")
#             _hash = sha1(user.email+_code_meta).hexdigest()
#             user.forget_pass_code = _hash
#             user.forget_pass_code_validity = _now +  datetime.timedelta(minutes=15)
#             user.save()
#             result['status'] = True
#             return Response(result)
#         else:
#             result['status'] = False
#             result['errors'] = s.errors
#             return Response(result,status=status.HTTP_400_BAD_REQUEST)


# class ForgotPassword(GenericAPIView):

#     serializer_class = serializers.ForgetPasswordSerializer
#     parser_classes = ((JSONParser,))

#     def post(self,request,*args,**kwargs):
#         data = request.data
#         s = serializers.ForgetPasswordSerializer(data=data)
#         result = dict()
#         if s.is_valid():
#             email = s.validated_data['email']
#             key = s.validated_data['key']
#             password = s.validated_data['new_password']
#             print timezone.now()
#             user = models.Users.objects.filter(email=email,forget_pass_code=key)
#             user = get_object_or_404(user)
#             if user.forget_pass_code_validity > timezone.now():
#                 user.forget_pass_code = None
#                 user.forget_pass_code_validity = None
#                 user.set_password(password)
#                 user.save()
#                 result['status'] = True
#             else:
#                 result['status']= False
#                 result['error'] = "Token Expired"
#             return Response(result)
#         else:
#             result['status'] = False
#             result['errors'] = s.errors
#             return Response(result,status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):

    def delete(self,request,*args,**kwargs):
        result = dict()
        result['status'] = True
        if request.user.is_authenticated():
            models.Token.objects.filter(user=request.user).delete()
            return Response(result,status=status.HTTP_200_OK)
        else:
            return Response(result,status=status.HTTP_200_OK)
