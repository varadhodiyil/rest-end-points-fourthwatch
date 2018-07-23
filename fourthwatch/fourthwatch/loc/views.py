# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView , ListAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from fourthwatch.loc import models, serializers , class_loc
from fourthwatch.auth_core import models as auth_models

# Create your views here.


	

class InitiateLOC(GenericAPIView):
	serializer_class = serializers.InitiateLOCSerializer
	parser_classes = ((JSONParser,MultiPartParser))
	
	def get(self,request , *args , **kwargs):
		user = request.user
		result = dict()
		if user.is_authenticated():
			result['status'] = True
			if type(user.user_type) == auth_models.Customer:
				data = models.LOC.objects.filter(Q(applicant=user) | Q(beneficiary=user))
				result_loc = list()
				for d in data:
					result_loc.append(class_loc.InitialLOC().get(d.id))
				result['result'] = result_loc
			elif type(user.user_type) == auth_models.BankEmployee:
				res = dict()
				bank_customers = auth_models.Customer.objects.filter(bank=user.user_type.bank)
				_bank_customer = list()
				for b in bank_customers:
					_b =  b.user.filter()
					if _b.count() > 0:
						_bank_customer.append(_b.get())
				data = models.LOC.objects.filter(applicant__in = _bank_customer)
				result_loc = list()
				for d in data:
					result_loc.append(class_loc.InitialLOC().get(d.id))
				res['buyer'] = result_loc

				bank_customers = auth_models.Customer.objects.filter(bank=user.user_type.bank)
				_bank_customer = list()
				for b in bank_customers:
					_b =  b.user.filter()
					if _b.count() > 0:
						_bank_customer.append(_b.get())
				
				data = models.LOC.objects.filter(beneficiary__in = _bank_customer)
				
				result_loc = list()
				for d in data:
					result_loc.append(class_loc.InitialLOC().get(d.id))
				res['seller'] = result_loc
				result['result'] = res
			
			return Response(result,status = status.HTTP_201_CREATED)
		else:
			result['status'] = False
			result['error'] = "Unauthorized!"
			return Response(result,status = status.HTTP_401_UNAUTHORIZED)
			
	def post(self,request,*args, **kwargs):
		user = request.user
		result = dict()
		if user.is_authenticated():
			data_req = request.data.copy()
			data_req['applicant'] = user.id
			s = self.get_serializer(data=data_req)
			if s.is_valid():
				product = s.validated_data.pop("product")
				rules = []
				instance = s.save()
				result['status'] = True
				#instance.delete()
				from_composer = class_loc.InitialLOC().create(instance.id,user.id,s.validated_data['beneficiary'].id,\
						[],product,request.build_absolute_uri(instance.locFile.url),\
						user.user_type.bank,s.validated_data['beneficiary'].user_type.bank)
				result['result'] = from_composer
				notification = dict()
				notification['text'] = "%s has submitted an LOC document. Please Click here to review" % user.first_name
				notification['loc'] = instance
				notification['notification_to'] = s.validated_data['beneficiary']

				models.Notifications(**notification).save()
				applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank = user.user_type.bank,is_admin=False)
				for a in applicant_bank_employee:
					user_obj =  a.user.get()
					notification['notification_to'] = user_obj
					models.Notifications(**notification).save()
				
				applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank = s.validated_data['beneficiary']\
							.user_type.bank,is_admin=False)
				for a in applicant_bank_employee:
					user_obj =  a.user.get()
					notification['notification_to'] = user_obj
					models.Notifications(**notification).save()

				notification = dict()
				notification['text'] = "You have submitted a LOC Document for Review. "
				notification['loc'] = instance
				notification['notification_to'] = user

				models.Notifications(**notification).save()
				return Response(result,status = status.HTTP_201_CREATED)
			else:
				result['status'] = False
				result['errors'] = s.errors
				return Response(result,status = status.HTTP_400_BAD_REQUEST)
		else:
			result['status'] = False
			result['error'] = "Unauthorized!"
			return Response(result,status = status.HTTP_401_UNAUTHORIZED)

class Notifications(GenericAPIView):
	serializer_class = serializers.NotificationSerializer

	def get(self, request , *args , **kwargs):
		user = request.user
		result = dict()
		if user.is_authenticated():
			result['status'] = True
			data = models.Notifications.objects.filter(notification_to=user)
			result['result'] = self.get_serializer(data,many=True).data
			return Response(result,status = status.HTTP_200_OK)
		else:
			result['status'] = False
			result['error'] = "Unauthorized!"
			return Response(result,status = status.HTTP_401_UNAUTHORIZED)