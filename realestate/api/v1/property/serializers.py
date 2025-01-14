from rest_framework import serializers
from property.models import Property, PropertyImage, Shortlist

class PropertySerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['property_id', 'user', 'latitude', 'longitude', 'city', 'price', 'property_type', 
                  'room_count', 'status', 'admin_approved', 'created_at', 'updated_at', 'images']
        read_only_fields = ['property_id', 'created_at', 'updated_at', ]

    def get_images(self, obj):
        try:
            # Retrieve all images related to the property
            property_images = PropertyImage.objects.filter(property=obj)
            request = self.context.get('request')

            # Build absolute URLs for each image
            images_urls = [
                request.build_absolute_uri(image.image.url) for image in property_images if image.image and image.image.url
            ]
            return images_urls
        except Exception as e:
            return None
    
    from rest_framework import serializers

class ShortlistSerializer(serializers.ModelSerializer):
    properties = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), many=True)

    class Meta:
        model = Shortlist
        fields = ['properties']
