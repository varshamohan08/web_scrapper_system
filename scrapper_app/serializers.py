from .models import EntitiesMaster
from rest_framework import serializers
from datetime import datetime
import json

class EntitiesMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntitiesMaster
        fields = '__all__'

    def create(self, validated_data):
        validated_data['details_json'] = json.dumps(validated_data['details_json'])
        entitiesMaster = EntitiesMaster.objects.create(**validated_data)
        return entitiesMaster

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['details_json'] = json.loads(instance.details_json)
        representation['created_date'] = instance.created_date.strftime('%a, %b %d, %Y %I:%M %p')
        return representation