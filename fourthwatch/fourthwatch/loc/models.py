# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from fourthwatch.auth_core.models import Users
# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.applicant.id, filename)	
class LOC(models.Model):
	objects = models.Manager()
	@property
	def product(self):
		return dict()
	id = models.AutoField(primary_key=True)
	applicant = models.ForeignKey(Users,related_name='applicant')
	beneficiary = models.ForeignKey(Users,related_name='beneficiary')
	locFile = models.FileField(upload_to=user_directory_path)
	updated_at = models.DateTimeField(auto_now=True)


class Notifications(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)
	text = models.TextField()
	sent_at = models.DateTimeField(auto_now=True)
	seen_at = models.DateTimeField(null=True)
	notification_to = models.ForeignKey(Users,on_delete=models.CASCADE)
	loc = models.ForeignKey(LOC,on_delete=models.CASCADE)


class Transaction(models.Model):
	objects = models.Manager()

	id = models.AutoField(primary_key=True)
	loc = models.ForeignKey(LOC,on_delete=models.CASCADE)
	party = models.ForeignKey(Users,on_delete=models.CASCADE)
	type = models.CharField(max_length=20)