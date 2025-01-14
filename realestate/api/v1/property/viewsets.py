from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from property.models import Property, PropertyImage, Shortlist
from .serializers import PropertySerializer
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from math import radians, cos, sin, sqrt, atan2
from rest_framework import status


class PropertyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


from django.db.models import F

from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Cos, Sin, Radians
from django.db.models import Value

class PropertyViewSet(ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PropertyPagination

    def haversine_query_expression(self, latitude, longitude):
        """
        Generate the Haversine expression for calculating distance in the database.
        """
        R = 6371  # Earth radius in kilometers

        # Convert degrees to radians
        lat1 = Radians(Value(float(latitude)))
        lon1 = Radians(Value(float(longitude)))
        lat2 = Radians(F('latitude'))
        lon2 = Radians(F('longitude'))

        # Haversine formula components
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (Sin(dlat / 2) ** 2) + Cos(lat1) * Cos(lat2) * (Sin(dlon / 2) ** 2)
        c = 2 * R * Radians(a ** 0.5)

        # Wrap the calculation with ExpressionWrapper to cast the result to a FloatField
        return ExpressionWrapper(c, output_field=FloatField())

    def get_queryset(self):
        queryset = Property.objects.filter(admin_approved=True)
        price_min = self.request.query_params.get('min_price')
        price_max = self.request.query_params.get('max_price')
        city = self.request.query_params.get('city')
        status = self.request.query_params.get('status', 'available')
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius', 10)
        sort_by = self.request.query_params.get('sort_by', 'price')  # Changed default to 'price'

        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if status:
            queryset = queryset.filter(status=status)

        # If latitude and longitude are provided, filter by distance
        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                radius = float(radius)
            except ValueError:
                raise ValidationError("Invalid latitude, longitude, or radius values.")

            # Annotate the queryset with distance
            distance_expr = self.haversine_query_expression(latitude, longitude)
            queryset = queryset.annotate(distance=distance_expr)
            queryset = queryset.filter(distance__lte=radius)
            
            if sort_by == 'proximity':
                queryset = queryset.order_by('distance')
        
        # If we're not sorting by distance or don't have distance annotation, sort by price
        if sort_by != 'proximity' or not (latitude and longitude):
            queryset = queryset.order_by('price')

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Handle the listing of properties with filters, sorting, and pagination.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data})

    def create(self, request, *args, **kwargs):
        """
        Handle property creation with multiple images.
        """
        data = request.data.copy()
        data['user'] = request.user.id
        data['admin_approved'] = False  # Ensure properties are not admin approved by default

        # Validate and save property
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        property_obj = serializer.save()

        # Handle multiple images
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)

        return Response({
            "property_id": property_obj.property_id,
            "message": "Property created successfully."
        }, status=201)


    def update(self, request, *args, **kwargs):
        """
        Handle property updates, restricting editable fields.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Ensure the user is the owner of the property
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to update this property.")

        # Restrict editable fields
        allowed_fields = ['price', 'details', 'status', 'room_count']
        update_data = {field: value for field, value in request.data.items() if field in allowed_fields}

        if not update_data:
            return Response({"error": "No valid fields to update."}, status=400)

        # Validate and save updates
        serializer = self.get_serializer(instance, data=update_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Property updated successfully."})


class ShortlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Add a property to the user's shortlist.
        Expects: { "property_id": <int> }
        """
        property_id = request.data.get('property_id')
        if not property_id:
            raise ValidationError({"error": "Property ID is required."})

        property_obj = get_object_or_404(Property, pk=property_id)

        # Retrieve or create the shortlist for the user
        shortlist, created = Shortlist.objects.get_or_create(user=request.user)
        shortlist.properties.add(property_obj)

        return Response({"message": "Property added to shortlist."}, status=201)

    def get(self, request):
        """
        Retrieve all properties in the user's shortlist.
        """
        shortlist = Shortlist.objects.filter(user=request.user).first()
        if not shortlist:
            return Response({"properties": []}, status=200)

        # Serialize the properties in the shortlist
        properties = shortlist.properties.all()
        serializer = PropertySerializer(properties, many=True, context={'request': request})

        return Response({"properties": serializer.data}, status=200)
    
    def delete(self, request):
        """
        Remove a property from the user's shortlist.
        Expects: { "property_id": <int> }
        """
        property_id = request.data.get('property_id')
        if not property_id:
            raise ValidationError({"error": "Property ID is required."})

        property_obj = get_object_or_404(Property, pk=property_id)

        # Retrieve the shortlist for the user
        shortlist = Shortlist.objects.filter(user=request.user).first()
        if not shortlist:
            return Response({"error": "No properties in shortlist."}, status=400)

        shortlist.properties.remove(property_obj)
        return Response({"message": "Property removed from shortlist."}, status=200)


class UserPortfolioAPIView(APIView):
    """
    API View to fetch all properties of the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get all properties owned by the authenticated user.
        """
        # Filter properties based on the logged-in user
        user_properties = Property.objects.filter(user=request.user)

        # If no properties are found
        if not user_properties:
            return Response({"detail": "No properties found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the properties
        serializer = PropertySerializer(user_properties, many=True)

        # Return serialized properties
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)