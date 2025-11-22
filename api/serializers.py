from rest_framework import serializers
from realrupees_app.models import *

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class AddPropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True)

    state = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    locality = serializers.StringRelatedField()

    class Meta:
        model = Add_Property
        fields = [
            'id', 'heading', 'subheading', 'property_id',
            'state', 'district', 'locality', 'paragraph',
            'youtube_url', 'google_map_link', 'price',
            'status', 'type', 'images'
        ]


class BlogContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Content
        fields = ['id', 'image', 'heading', 'paragraph', 'date']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State_name
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    class Meta:
        model = District_name
        fields = ['id', 'name', 'state']


class LocalitySerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    district = serializers.StringRelatedField()

    class Meta:
        model = Locality
        fields = ['id', 'name', 'state', 'district']


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'title', 'description', 'video', 'type']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'review']



class ContactUspageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Uspage
        fields = '__all__'