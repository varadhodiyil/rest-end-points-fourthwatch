# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey , GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from hashlib import sha1
# Create your models here.

import datetime
TOKEN_EXPIRE_TIME = datetime.timedelta(days=30)

class Users(AbstractUser):
    @property
    def name(self):
        return self.first_name + " " + self.last_name
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    user_type = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = "users"

class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,unique=True)


class BankEmployee(models.Model):
    objects = models.Manager()
    
    id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    user = GenericRelation(Users)

class Customer(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    user = GenericRelation(Users)



class TokenManager(models.Manager):
    def delete_session(self, *args, **kwargs):
        if "key" in kwargs:
            tokent_str = kwargs['key']
            Token.objects.filter(key=tokent_str).delete()
        return True

    def is_valid(self, *args, **kwargs):

        if "key" in kwargs:
            tokent_str = kwargs['key']
            Token.objects.filter(
                key=tokent_str, expires_at__lte=timezone.now()).delete()
            tokens = Token.objects.filter(
                key=tokent_str, expires_at__gte=timezone.now()).get()
        return tokens


class Token(models.Model):
    user = models.ForeignKey(Users)
    key = models.CharField(primary_key=True, max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=None)
	
    objects = TokenManager()

    class Meta:
        db_table = 'access_tokens'
        db_tablespace = 'default'

    def save(self, *args, **kwargs):
        user_id_str = self.user.id
        self.expires_at = timezone.now() + TOKEN_EXPIRE_TIME
        exists, self.key = self.generate_key(user_id_str)
        if not exists:
            super(Token, self).save(*args, **kwargs)

        return self

    def generate_key(self, id_):
        existing_token = None
        exists = True
        tokens = Token.objects.filter(
            user_id=id_, expires_at__gte=timezone.now()).values("key")
        for token in tokens:
            existing_token = token['key']
            token = existing_token
        if existing_token is None:
            exists = False
            token = sha1(id_.__str__() + str(timezone.now())).hexdigest()
            Token.objects.filter(
                user=id_, expires_at__lte=timezone.now()).delete()
        return exists, token
