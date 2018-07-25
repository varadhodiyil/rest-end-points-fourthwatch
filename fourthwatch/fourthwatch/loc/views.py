# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from django.utils import timezone
from fourthwatch.loc import models, serializers, class_loc
from fourthwatch.auth_core import models as auth_models
from django.shortcuts import get_object_or_404

# Create your views here.


class LOCAPI(GenericAPIView):
    serializer_class = serializers.InitiateLOCSerializer
    parser_classes = ((JSONParser, MultiPartParser))

    def get(self, request, id, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            result['status'] = True
            if type(user.user_type) == auth_models.Customer:

                data = models.LOC.objects.filter(
                    Q(applicant=user) | Q(beneficiary=user), id=id)
                data = get_object_or_404(data)
                result_loc = list()
                result_loc.append(class_loc.InitialLOC().get(data.id))
                result['result'] = result_loc
            elif type(user.user_type) == auth_models.BankEmployee:
                res = dict()
                bank_customers = auth_models.Customer.objects.filter(
                    bank=user.user_type.bank)
                _bank_customer = list()
                for b in bank_customers:
                    _b = b.user.filter()
                    if _b.count() > 0:
                        _bank_customer.append(_b.get())
                data = models.LOC.objects.filter(
                    applicant__in=_bank_customer, id=id)
                result_loc = list()
                for d in data:
                    result_loc.append(class_loc.InitialLOC().get(d.id))
                res['buyer'] = result_loc

                bank_customers = auth_models.Customer.objects.filter(
                    bank=user.user_type.bank)
                _bank_customer = list()
                for b in bank_customers:
                    _b = b.user.filter()
                    if _b.count() > 0:
                        _bank_customer.append(_b.get())

                data = models.LOC.objects.filter(
                    beneficiary__in=_bank_customer, id=id)

                result_loc = list()
                for d in data:
                    result_loc.append(class_loc.InitialLOC().get(d.id))
                res['seller'] = result_loc
                result['result'] = res

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class InitiateLOC(GenericAPIView):
    serializer_class = serializers.InitiateLOCSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            result['status'] = True
            if type(user.user_type) == auth_models.Customer:
                data = models.LOC.objects.filter(
                    Q(applicant=user) | Q(beneficiary=user))
                result_loc = list()

                for d in data:
                    names = dict()
                    names['applicant_name'] = d.applicant.name
                    names['beneficiary_name'] = d.beneficiary.name
                    __data = class_loc.InitialLOC().get(d.id)
                    has_approved = models.Transaction.objects.filter(
                        party=user, type="APPROVE")
                    if has_approved.count() > 0:
                        names['has_approved'] = True
                    else:
                        names['has_approved'] = False
                    
                    if d.applicant == user:
                        names['is_applicant'] = True
                        names['is_beneficiary'] = False
                    if d.beneficiary == user:
                        names['is_beneficiary'] = True
                        names['is_applicant']  = False
                    
                    __data.update(names)
                    result_loc.append(__data)
                result['result'] = result_loc
            elif type(user.user_type) == auth_models.BankEmployee:
                res = dict()
                bank_customers = auth_models.Customer.objects.filter(
                    bank=user.user_type.bank)
                _bank_customer = list()
                for b in bank_customers:
                    _b = b.user.filter()
                    if _b.count() > 0:
                        _bank_customer.append(_b.get())
                data = models.LOC.objects.filter(applicant__in=_bank_customer)
                result_loc = list()
                for d in data:
                    names = dict()
                    names['applicant_name'] = d.applicant.name
                    names['beneficiary_name'] = d.beneficiary.name
                    __data = class_loc.InitialLOC().get(d.id)
                    __data.update(names)
                    result_loc.append(__data)
                res['buyer'] = result_loc

                bank_customers = auth_models.Customer.objects.filter(
                    bank=user.user_type.bank)
                _bank_customer = list()
                for b in bank_customers:
                    _b = b.user.filter()
                    if _b.count() > 0:
                        _bank_customer.append(_b.get())

                data = models.LOC.objects.filter(
                    beneficiary__in=_bank_customer)

                result_loc = list()
                for d in data:
                    names = dict()
                    names['applicant_name'] = d.applicant.name
                    names['beneficiary_name'] = d.beneficiary.name
                    __data = class_loc.InitialLOC().get(d.id)
                    __data.update(names)
                    result_loc.append(__data)
                    result_loc.append(__data)
                res['seller'] = result_loc
                result['result'] = res

            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data_req = request.data.copy()
            data_req['applicant'] = user.id
            s = self.get_serializer(data=data_req)
            if s.is_valid():
                product = s.validated_data.pop("product")
                rules = s.validated_data.pop("rules")
                _rules = list()
                for i, r in enumerate(rules):
                    r['id'] = i
                    r['$class'] = "org.fourthwatch.Rule"
                    r['rultText'] = r['ruleText']
                    _rules.append(r)
                instance = s.save()
                result['status'] = True
                # instance.delete()
                from_composer = class_loc.InitialLOC().create(instance.id, user.id, s.validated_data['beneficiary'].id,
                                                              _rules, product, request.build_absolute_uri(
                                                                  instance.locFile.url),
                                                              user.user_type.bank.id, s.validated_data['beneficiary'].user_type.bank.id)
                result['result'] = from_composer
                notification = dict()
                notification['text'] = "%s has submitted an LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance
                notification['notification_to'] = s.validated_data['beneficiary']

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    if a.user.count() > 0:
                        user_obj = a.user.get()
                        notification['notification_to'] = user_obj
                        models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=s.validated_data['beneficiary']
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    if a.user.count() > 0:
                        user_obj = a.user.get()
                        notification['notification_to'] = user_obj
                        models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have submitted a LOC Document for Review. "
                notification['loc'] = instance
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class Notifications(GenericAPIView):
    serializer_class = serializers.NotificationSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            result['status'] = True
            data = models.Notifications.objects.filter(notification_to=user)
            result['result'] = self.get_serializer(data, many=True).data
            return Response(result, status=status.HTTP_200_OK)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class ApproveAPI(GenericAPIView):
    serializer_class = serializers.ApproveSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "APPROVE"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():
                instance = s.save()
                result['status'] = True
                result['result'] = class_loc.Approve().create(
                    instance.loc.id, instance.party.id, instance.party)
                notification = dict()
                notification['text'] = "%s has Approved an LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Approved a LOC Document. "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class RejectAPI(GenericAPIView):
    serializer_class = serializers.RejectSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "REJECT"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():

                result['status'] = True
                closeReason = s.validated_data['closeReason']
                s.validated_data.pop('closeReason')
                instance = s.save()
                result['result'] = class_loc.Reject().create(
                    instance.loc.id, instance.party.id, instance.party, closeReason)
                notification = dict()
                notification['text'] = "%s has Rejected an LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Rejected a LOC Document. "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class ShipProductAPI(GenericAPIView):
    serializer_class = serializers.ShipProductSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "SHIPPRODUCT"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():
                result['status'] = True
                evidence = s.validated_data['evidence']
                s.validated_data.pop('evidence')
                instance = s.save()
                result['result'] = class_loc.ShipProduct().create(
                    instance.loc.id, instance.party.id, instance.party, evidence)
                notification = dict()
                notification['text'] = "%s has Shipped products an LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Shipped  products a LOC Document. "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class ReceiveProductAPI(GenericAPIView):
    serializer_class = serializers.TransactionSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "RECEIVEPRODUCT"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():
                result['status'] = True
                instance = s.save()
                result['result'] = class_loc.ReceiveProduct().create(
                    instance.loc.id, instance.party.id, instance.party)
                notification = dict()
                notification['text'] = "%s has Received product LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Received the product for LOC Document. "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class ReadyForPaymentAPI(GenericAPIView):
    serializer_class = serializers.TransactionSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "READYFORPAYMENT"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():
                instance = s.save()
                result['status'] = True
                result['result'] = class_loc.ReadyForPayment().create(
                    instance.loc.id, instance.party.id, instance.party)
                notification = dict()
                notification['text'] = "%s has Received product LOC document. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Received the product for LOC Document. "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class CloseAPI(GenericAPIView):
    serializer_class = serializers.CloseSerializer
    parser_classes = ((JSONParser, FormParser))

    def post(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            data = request.data.copy()
            data['type'] = "CLOSE"
            data['party'] = user.id
            s = self.get_serializer(data=data)
            if s.is_valid():
                result['status'] = True
                closeReason = s.validated_data['closeReason']
                s.validated_data.pop('closeReason')
                instance = s.save()
                result['result'] = class_loc.PaymentReceived().create(
                    instance.loc.id, instance.party.id, instance.party, closeReason)
                notification = dict()
                notification['text'] = "%s has Closed the  LOC document Transaction. Please Click here to review" % user.first_name
                notification['loc'] = instance.loc
                notification['notification_to'] = instance.loc.beneficiary

                models.Notifications(**notification).save()
                applicant_bank_employee = auth_models.BankEmployee.objects.filter(
                    bank=user.user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                applicant_bank_employee = auth_models.BankEmployee.objects.filter(bank=instance.loc.beneficiary
                                                                                  .user_type.bank, is_admin=False)
                for a in applicant_bank_employee:
                    user_obj = a.user.get()
                    notification['notification_to'] = user_obj
                    models.Notifications(**notification).save()

                notification = dict()
                notification['text'] = "You have Closed the  LOC Document. Transaction "
                notification['loc'] = instance.loc
                notification['notification_to'] = user

                models.Notifications(**notification).save()
                return Response(result, status=status.HTTP_200_OK)
            else:
                result['status'] = False
                result['errors'] = s.errors
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class Customers(GenericAPIView):
    serializer_class = serializers.CustomerSerializer
    pagination_class = ((JSONParser, FormParser))

    def get(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            _users = auth_models.Customer.objects.all()
            users = list()
            for u in _users:
                users.extend(u.user.filter().exclude(id=user.id))
            result['status'] = True
            result['result'] = self.get_serializer(users, many=True).data
            return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)


class NotificationMarkRead(GenericAPIView):
    serializer_class = serializers.CustomerSerializer
    pagination_class = ((JSONParser, FormParser))

    def get(self, request, *args, **kwargs):
        user = request.user
        result = dict()
        if user.is_authenticated():
            _users = models.Notifications.objects.filter(
                notification_to=user).update(seen_at=timezone.now())
            result['status'] = True
            return Response(result)
        else:
            result['status'] = False
            result['error'] = "Unauthorized!"
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
