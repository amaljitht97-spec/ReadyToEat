from django.db import models
from account.models import User
from django.db.models.signals import post_save
from donor.models import *


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="custmomer_profile")
    phone=models.CharField(max_length=15)
    address=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
def create_custmer_profile(sender, instance, created, **kwargs):
    if created and instance.role=="customer":
       Customer.objects.create(user=instance)
post_save.connect(create_custmer_profile,User)

class CustomerFoodcategory(models.Model):
     title=models.CharField(max_length=100)
     bio=models.CharField(max_length=100)
     image=models.ImageField(upload_to="Food-customer")
     def __str__(self):
        return self.title

class FoodRequestModel(models.Model):
    food=models.ForeignKey(FoodDonorModel,on_delete=models.CASCADE,related_name="requests_food_customers")
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="requests_users_customer")
    food_images = models.ImageField(
    upload_to="fooddonor_image",
    default="fooddonor_image/default.jpg")  
    quantity=models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    status=models.CharField(max_length=20,choices=[('pending','Pending'),('accepted','Accepted'),('rejected','rejected'),('completed','completed')],default='pending')
    rating = models.IntegerField(null=True, blank=True)   
    review = models.TextField(null=True, blank=True)
    requested_at=models.DateTimeField(auto_now_add=True)

class CartModel(models.Model):
    food_cart=models.ForeignKey(FoodDonorModel,on_delete=models.CASCADE,related_name="cart_food")
    price = models.DecimalField(decimal_places=2, max_digits=6)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    food_imagescart=models.ImageField(upload_to="foodcustomer_image",default="fooddonor_image/default.jpg")
    quantity=models.IntegerField()
    status=models.CharField(max_length=20,choices=[('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')],default='pending')
    requested_at=models.DateTimeField(auto_now_add=True)

    @property
    def food_total(self):
        total=self.food_cart.price*self.quantity
        return total
    

class Order(models.Model):
    STATUS_CHOICES=(
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('pickedup','Pickedup'),
        ('delivered','Delivered'),

    )
    food_order=models.ManyToManyField(FoodDonorModel,related_name="enrolleds_order")
    order_user=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="orders")
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="pendings")
    total=models.DecimalField(max_digits=10,decimal_places=2)
    is_paid=models.BooleanField(default=False)
    razer_pay_order_id=models.CharField(max_length=100,null=True)
    total_quantity=models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review=models.CharField()

    def __str__(self):
        return str(self.razer_pay_order_id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(FoodDonorModel, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Review(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        FoodDonorModel,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    comment = models.TextField()

    rating = models.IntegerField(default=5)  

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.food}"
    

