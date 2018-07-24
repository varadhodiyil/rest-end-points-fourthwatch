from rest_framework import serializers
from fourthwatch.loc.models import LOC , Notifications , Transaction
from django.utils import timesince
from fourthwatch.auth_core.models import Users

class ProductSerializer(serializers.Serializer):
	type = serializers.CharField()
	quantity = serializers.IntegerField()
	pricePerUnit = serializers.FloatField()
	
	class Meta:
		fields = '__all__'

class RulesSerializer(serializers.Serializer):
	ruleText = serializers.CharField()
	class Meta:
		fields = '__all__'
class InitiateLOCSerializer(serializers.ModelSerializer):
	product = ProductSerializer()
	rules = RulesSerializer(required=False,many=True)
	class Meta:
		model = LOC
		fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		data = super(NotificationSerializer, self).to_representation(instance)
		data['sent_at'] = timesince.timesince(instance.sent_at)
		return data
	class Meta:
		model = Notifications
		fields = '__all__'


class ApproveSerializer(serializers.ModelSerializer):
	
	class Meta:
		fields = '__all__'
		model = Transaction

class RejectSerializer(serializers.ModelSerializer):
	closeReason = serializers.CharField()
	class Meta:
		fields = '__all__'
		model = Transaction

class ShipProductSerializer(serializers.ModelSerializer):
	evidence = serializers.CharField()
	class Meta:
		fields = '__all__'
		model = Transaction


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Transaction

class CloseSerializer(serializers.ModelSerializer):
	closeReason = serializers.CharField()
	class Meta:
		fields = '__all__'
		model = Transaction

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		fields = ['first_name','last_name','id','name']
		model = Users