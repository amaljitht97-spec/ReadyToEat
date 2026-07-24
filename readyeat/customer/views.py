from django.shortcuts import render,redirect,get_object_or_404
from account.models import *
from customer.forms import *
from django.views import View
from django.contrib import messages
from django.views.generic import *
from donor.models import *
from customer.models import *
from decimal import Decimal
from django.views import View
from django.db import transaction
import razorpay
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import razorpay

# import razorpay

RAZR_KEY_ID="rzp_test_SgrwntEK0DQqxH"

RAZR_SECRET_KEY="uQqqHe5i3LgRSYbi3HzjFwA2"

# Create your views here.

class CustomerRegisterView(View):
    def get(self,request):
        form=CustomerRegistrationForm
        return render(request,"customerreg.html",{"form":form})
    def post(self,request):
        form_data=CustomerRegistrationForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"successfully Registered!")
            return redirect('homedash')
        return render(request,"customerreg.html",{"form":form_data})
    
class CustomerLoginView(View):
    def get(self,request):
        return render(request,"customerlogin.html")


    
class CustomerProfileView(View):

    def get(self, request):
        profile, created = Customer.objects.get_or_create(
            user=request.user   
        )

        form = CustomerForm(instance=profile)
        return render(request, "customerprofile.html", {"form": form,
                                                        "id":profile.id
                                                        })


    def post(self, request):
        profile, created = Customer.objects.get_or_create(
            user=request.user   
        )

        form = CustomerForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('customerfoods')

        return render(request, "customerprofile.html", {"form": form})
    
class FoodCategoryCustomerViews(View):
    def get(self,request):
        qs=FoodCategory.objects.all()
        return render(request,"customerfood.html",{"data":qs})
    def post(self,request):
        
      user = request.user  
      fid = request.POST.get('id')
      if not fid:
         messages.error(request, "ID not received")
         return redirect('customerfoods')

      if user.role == "donor":
        return redirect('fooddonor')

      elif user.role == "customer":
        return redirect('foodlist', id=int(fid))  

      else:
        messages.info(request, "not user")
        return redirect('customerfoods')
    
    # template_name="customerfood.html"
    # queryset=FoodCategory.objects.all()
    # context_object_name="data"

    # def get_queryset(self):
    #     return super().get_queryset()
    
    


    
# class FoodItemsView(ListView): 
#     template_name="donorfoods.html" 
#     queryset=FoodDonorModel.objects.all() 
#     context_object_name="data"
    
     
#     def get_queryset(self,**kwargs): 
#         qs=super().get_queryset() 
#         cat=FoodCategory.objects.get(id=self.kwargs.get('id')) 
#         return qs.filter(food_items=cat)


from django.views.generic import ListView
from django.db.models import Prefetch

class FoodItemsView(ListView):
    template_name = "donorfoods.html"
    context_object_name = "data"

    def get_queryset(self):
        cat = FoodCategory.objects.get(id=self.kwargs.get('id'))

        return FoodDonorModel.objects.filter(
            food_items=cat
        ).prefetch_related('reviews')
  
        
        
    
    


#    def get(self, request, pk):
#        data = FoodDonorModel.objects.get(id=pk)
#        customer = Customer.objects.get(user=request.user)
#        try:
           
#           obj,created = FoodRequestModel.objects.get_or_create(
#             user=customer,
#             food=data,
#               defaults={"quantity": 1,
#                 "food_images": data.food_images.name  })
       
#           return render(request,"customersrequest.html",{"data":data})
#        except:
#            messages.info(request,"need more foods ")
#            return redirect('homedash') 



# class FoodRequestView(View):
#     def get(self,request,**kwargs):
#         cid=kwargs.get('pk')
#         data=FoodDonorModel.objects.get(id=cid)
#         customer = Customer.objects.get(user=request.user)
        
#         try:
#             obj,created=CartModel.objects.get_or_create(
#                 food_cart=data,
#                 customer=customer)
#             return redirect('cartlist')
#         except:
#             messages.info(request,"Courses Already Added to Cart !!")
#             return render(request,'foodrequest',{"food":data,})
    


class FoodRequestView(View):

    def post(self, request, *args, **kwargs):
        cid = kwargs.get('pk')
        data = FoodDonorModel.objects.get(id=cid)
        customer = Customer.objects.get(user=request.user)

        qty = int(request.POST.get("quantity", 1))

        obj, created = CartModel.objects.get_or_create(
            food_cart=data,
            customer=customer,
            defaults={
                'price': data.price,
                'quantity': qty
            }
        )

        if not created:
            obj.quantity += qty
            obj.price = data.price
            obj.save()
            messages.info(request, "Quantity updated in cart")
        else:
            messages.success(request, "Added to cart 🛒")

        return render(request,"customersrequest.html",{"data":data})
        
       

       


# class AddtoCartView(View):

#     def get(self, request, **kwargs):

#         aid = kwargs.get('pk')

#         data = FoodRequestModel.objects.get(id=aid) 

        
#         customer, created = Customer.objects.get_or_create(user=request.user)

#         cart_obj, _ = CartModel.objects.get_or_create(
#             customer=customer,
#             food_cart=data,
#             defaults={
#                 "quantity": 1,
#                 "food_imagescart": data.food_images
#             }
#         )

#         return render(request, "customercart.html", {
#             'data': data,
#             'obj': cart_obj
#         })
# class AddtoCartView(View):

#     def post(self, request, **kwargs):
#         aid = kwargs.get('pk')

#         data = get_object_or_404(FoodRequestModel, id=aid)

#         customer, _ = Customer.objects.get_or_create(user=request.user)

#         cart_obj, created = CartModel.objects.get_or_create(
#             customer=customer,
#             food_cart=data,
#             defaults={
#                 "quantity": 1,
#                 "food_imagescart": data.food_images
#             }
#         )

#         if not created:
#             cart_obj.quantity += 1
#             cart_obj.save()

#         return redirect('cartlist')  #
        

class AddtoCartView(View):

    def post(self, request, **kwargs):

        aid = kwargs.get('pk')
        data = get_object_or_404(FoodDonorModel, id=aid)

        customer, created = Customer.objects.get_or_create(user=request.user)

        cart_obj, created = CartModel.objects.get_or_create(
            customer=customer,
            food_cart=data,
            defaults={
                "quantity": 1,
                "food_imagescart": data.food_images
            }
        )

     
        if not created:
            cart_obj.quantity += 1
            cart_obj.save()

        return render(request,"customercart.html")  
class CartListView(View):

    def get(self, request):
        customer = Customer.objects.get(user=request.user)

        cart_items = CartModel.objects.filter(customer=customer)

        total = 0

        for item in cart_items:
            total += item.food_cart.price * item.food_cart.quantity
        print(total)  

        return render(request, "customercart.html", {
            "cart_items": cart_items,
            "total": total
        })
    def post(self, request):
        # handle add/update car
         customer = Customer.objects.get(user=request.user)
         cart_items = CartModel.objects.filter(customer=customer)

         total = 0

         for item in cart_items:
            total += item.food_cart.price * item.food_cart.quantity
         print(total)  

         return render(request, "customercart.html", {
            "cart_items": cart_items,
            "total": total
        })
  
 

class RemoveCartView(View):

    def get(self, request, pk):
        item = get_object_or_404(CartModel, id=pk)
        item.delete()

        return redirect('cartlist')
    
class DecreaseQtyView(View):
    def get(self, request, pk):
        # logic here
        return redirect('cartlist')

class IncreaseQtyView(View):
    def get(self, request, pk):
        cart_item = get_object_or_404(CartModel, id=pk)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cartlist')
from decimal import Decimal



# class CheckoutView(View):
#     def get(self, request):

#         if not request.user.is_authenticated:
#             return redirect('login')

#         customer, _ = Customer.objects.get_or_create(user=request.user)

#         qs = CartModel.objects.filter(customer=customer)

#         if not qs.exists():
#             return redirect('homedash')

#         cart_total = 0
#         total_quantity = 0

#         for item in qs:
#             cart_total += item.price * item.quantity
#             total_quantity += item.quantity

#         try:
#             with transaction.atomic():

                
#                 order = Order.objects.create(
#                     order_user=customer,
#                     total=cart_total,
#                     total_quantity=total_quantity
#                 )

                
#                 for item in qs:
#                     OrderItem.objects.create(
#                         order=order,
#                         food=item.food_cart,
#                         quantity=item.quantity,
#                         price=item.price
#                     )

                
#                 qs.delete()

#         except Exception as e:
#             print("Checkout Error:", e)
#             return redirect('cartlist')

#         return redirect('customerorder')


class PlaceOrderView(View):
    def get(self, request):

        customer = Customer.objects.get(user=request.user)
        qs = CartModel.objects.filter(customer=customer)

        cart_total = 0
        for i in qs:
            cart_total += i.food_cart.price * i.quantity

       
        order1 = Order.objects.create(
            order_user=customer,
            total=cart_total,
        )
        amount = int(cart_total * 100)
        
        for i in qs:
            order1.food_order.add(i.food_cart)

        qs.delete()
        if cart_total > 0:
            client = razorpay.Client(auth=(RAZR_KEY_ID,RAZR_SECRET_KEY))
            data = { "amount":amount, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            order1.razer_pay_order_id=payment.get('id')
            order1.save()
            context={
                "razr_key_id":RAZR_KEY_ID,
                "amount":amount,
                "razr_pay_id":payment.get('id')
                
            }
            return render(request,'payment.html',{"data":context})
        return redirect('customerorder')



# # @method_decorator(csrf_exempt,name="dispatch")     
# class PaymentPage(View):
#     def get(self,request):
#         return render(request,'payment.html')









# @method_decorator(csrf_exempt, name='dispatch')
# class PaymentVerify(View):
#     def post(self, request):
#         client = razorpay.Client(auth=(RAZR_KEY_ID, RAZR_SECRET_KEY))
#         try:
#             client.utility.verify_payment_signature(request.POST)
#             razr_pay_order_id=request.POST.get('razorpay_order_id')
#             order_instace=Order.objects.get(razer_pay_order_id=razr_pay_order_id)
#             order_instace.is_paid=True
#             order_instace.status="accepted"
#             order_instace.save()
#         except:
#               print("failed")
#               order_instace=Order.objects.get(razer_pay_order_id=razr_pay_order_id)
#               order_instace.is_paid=False
#               order_instace.status="rejected"
#         return redirect('customerorder')


@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerify(View):
    def post(self, request):
        client = razorpay.Client(auth=(RAZR_KEY_ID, RAZR_SECRET_KEY))

        razr_pay_order_id = request.POST.get('razorpay_order_id')
        razr_payment_id = request.POST.get('razorpay_payment_id')
        razr_signature = request.POST.get('razorpay_signature')

        if not razr_pay_order_id:
            return redirect('customerorder')

        params_dict = {
            'razorpay_order_id': razr_pay_order_id,
            'razorpay_payment_id': razr_payment_id,
            'razorpay_signature': razr_signature
        }

    
        order_instance = get_object_or_404(Order, razer_pay_order_id=razr_pay_order_id)

        try:
            client.utility.verify_payment_signature(params_dict)
            order_instance.is_paid = True
            order_instance.status = "accepted"

        except Exception as e:
            print("failed:", e)
            order_instance.is_paid = False
            order_instance.status = "rejected"

        order_instance.save()
        return redirect('customerorder')
       
       

       

class CustomerOrderView(View):
    def get(self, request, *args, **kwargs):
        customer=Customer.objects.get(user=request.user)
        order = Order.objects.filter(order_user=customer).last()

        return render(request, 'customerorderfood.html', {
            'order': order
        })
        
        
class OrderListView(View):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(order_user=customer)

        return render(request, "orderlist.html", {"orders": orders})


class orderView(View):
    def get(self, request, pk):
        customer = Customer.objects.get(user=request.user)
        

        order = get_object_or_404(
            Order,
            id=pk,
            order_user=customer
        )
        
        
            

        foods = order.food_order.all()
        # total = sum(item.price for item in foods)

        return render(request, "orderview.html", {
            "data": order,
            "foods": foods,
            # "total": total 
        })


class ReviewView(View):
    def post(self, request, pk):
        customer = Customer.objects.get(user=request.user)
        order = get_object_or_404(Order, id=pk, order_user=customer)

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = customer
            review.order = order

            food_id = request.POST.get("food_id")
            review.food_id = food_id

            review.save()

        return redirect("displayreview", pk=pk)


# class ReviewView(View):
#     def post(self, request, pk):
#         customer = Customer.objects.get(user=request.user)
#         order = get_object_or_404(Order, id=pk, order_user=customer)

#         form = ReviewForm(request.POST)

#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = customer
#             review.order = order

#             food_id = request.POST.get("food_id")
#             review.food_id = food_id

#             review.save()

#         return redirect("addreview", pk=pk)   
    

class DisplayReView(View):
    def get(self, request, pk):
        customer = Customer.objects.get(user=request.user)

        order = get_object_or_404(
            Order,
            id=pk,
            order_user=customer
        )

        foods = order.food_order.all()

        reviews = Review.objects.filter(order=order)

        form = ReviewForm()

        return render(request, "displayreview.html", {
            "order": order,
            "foods": foods,
            "reviews": reviews,
            "form": form
        })
        

class LocationView(View):
    def get(self, request, pk):

        # logged-in customer
        customer = Customer.objects.get(user=request.user)

        # get selected food
        food = get_object_or_404(FoodDonorModel, id=pk)

        # get donor from food
        donor = food.donor

        return render(request, "location.html", {
            "donor": donor,
            "food": food
        })
        
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')
    
        
        
        
       

 
   




