from rest_framework import serializers
from api.models import Property, PropertyAmenity, PropertyDescription


class PropertyDescriptionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = PropertyDescription
        fields =  "__all__"

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields =  "__all__"


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'