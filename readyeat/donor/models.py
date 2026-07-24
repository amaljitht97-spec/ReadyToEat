from django.db import models
from django.contrib.auth.models import AbstractUser
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# from donor.models import DonorProfile
# Create your models here.


class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
     return self.user.username
def create_profile(sender, instance, created, **kwargs):
    if created and instance.role=="donor":
       DonorProfile.objects.create(user=instance)
post_save.connect(create_profile,User)





class FoodCategory(models.Model):
    title=models.CharField(max_length=100)
    bio=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Food-img")
    def __str__(self):
        return self.title



class FoodItemModel(models.Model):
   donor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="food_item")
   organization_name=models.ForeignKey(DonorProfile,on_delete=models.CASCADE,related_name="organizer")
   food_items=models.ForeignKey(FoodCategory,on_delete=models.CASCADE)
   food_title=models.CharField(max_length=100)
   food_description=models.CharField(max_length=300)
   food_images=models.ImageField(upload_to="fooditem_image",null=True,default="course_images/defualt.png")
   quantity=models.IntegerField()
   is_free=models.BooleanField(default=False)
   price=models.DecimalField(decimal_places=2,max_digits=6)
   created_at=models.DateTimeField(auto_now_add=True)
   expairy_time=models.DateTimeField(auto_now=True)
   available=models.BooleanField(default=True)


class FoodModel(models.Model):
   
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foods")
    organization_name = models.CharField(max_length=200)
    food_items = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=100)
    food_description = models.CharField(max_length=300)
    food_images = models.ImageField(upload_to="fooditem_image", null=True,default="fooditem_image/default.png")
    quantity = models.IntegerField()
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expairy_time = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def get_organization_name(self):
       return self.donor.donorprofile.organization_name
    
class FoodDonorModel(models.Model):
   
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foods_donors")
    organization_name = models.CharField(max_length=200)
    food_items = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=100)
    food_description = models.CharField(max_length=300)
    food_images = models.ImageField(upload_to="fooddonor_image",default="fooddonor_image/default.jpg")
    quantity = models.IntegerField()
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expairy_time = models.DateTimeField()
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default="Available") 

    def get_organization_name(self):
       return self.donor.donorprofile.organization_name
    @property
    def is_available(self):
        print("Expeiry",self.expairy_time)
        print("Now",timezone.now())
        return self.available and self.quantity > 0 and self.expairy_time > timezone.now()
    
class Fooddisplay(models.Model):
    title=models.CharField(max_length=100)
    bio=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Food_donor",null=True,default="food_images1/default.jpg")

