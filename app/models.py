from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.gis.db import models
from geopy.distance import geodesic

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('waiter', "Waiter")
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    restaurant_location = models.PointField()
    
    def __str__(self):
        return self.name
    
    
class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/menu_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant_id = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),  
        ('accepted', 'Accepted'), 
        ('delivered', 'Delivered')]
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    
    def get_distance(self):
        restaurant_coords = (self.restaurant.restaurant_location.y, self.restaurant.restaurant_location.x)
        delivery_coords = (self.delivery_location.y, self.delivery_location.x)
        return geodesic(restaurant_coords, delivery_coords).kilometers