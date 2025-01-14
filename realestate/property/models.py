from django.db import models
from django.contrib.auth.models import User
import uuid
import os

# Create your models here.
def property_img_upload_dir(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    root_path = "backend/property_images"
    return os.path.join(root_path, filename)


class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=255)
    price = models.FloatField()
    property_type = models.CharField(max_length=10, choices=[('student', 'Student Accomodation'), ('private', 'Private Accomodation')])
    room_count = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('sold', 'Sold')])
    admin_approved = models.BooleanField(default=False)  # By default, not admin approved
    models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_type} - {self.city} - {self.price}"
    
class PropertyImage(models.Model):
    image = models.FileField(upload_to=property_img_upload_dir)
    property = models.ForeignKey(Property, related_name="property_image", on_delete=models.CASCADE)

class Shortlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shortlist")
    properties = models.ManyToManyField('Property', related_name="shortlisted_by")

    def __str__(self):
        return f"{self.user.username}'s Shortlist"