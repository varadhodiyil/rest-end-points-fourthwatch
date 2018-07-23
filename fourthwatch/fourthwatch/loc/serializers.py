from rest_framework import serializers
from fourthwatch.loc.models import LOC , Notifications
from django.utils import timesince

class ProductSerializer(serializers.Serializer):
	type = serializers.CharField()
	quantity = serializers.IntegerField()
	pricePerUnit = serializers.FloatField()
	
	class Meta:
		fields = '__all__'
class InitiateLOCSerializer(serializers.ModelSerializer):
	product = ProductSerializer()
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