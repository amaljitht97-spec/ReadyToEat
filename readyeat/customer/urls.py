from django.urls import path
from customer.views import *

urlpatterns=[
    path('customersign',CustomerRegisterView.as_view(),name="custsign"),
    path('customerprofile',CustomerProfileView.as_view(),name="customerprofile"),
    path('customerfoods',FoodCategoryCustomerViews.as_view(),name="customerfoods"),
    
    path('foodlist/<int:id>',FoodItemsView.as_view(),name="foodlist"),
    path('foodrequest/<int:pk>',FoodRequestView.as_view(),name="foodrequest"),
    path('addcart/<int:pk>',AddtoCartView.as_view(),name="addcart"),
    path('cartlist',CartListView.as_view(),name="cartlist"),
    path('remove-cart/<int:pk>/', RemoveCartView.as_view(), name='remove_cart'),
    path('decrease-qty/<int:pk>/',DecreaseQtyView.as_view(), name='decrease_qty'),
    path('increase-qty/<int:pk>/',IncreaseQtyView.as_view(), name='increase_qty'),
    # path('checkout',CheckoutView.as_view(), name='checkout'),
    path('placeorder',PlaceOrderView.as_view(),name="placeorder"),
    path('pay-verify/',PaymentVerify.as_view(),name="pay-verify"),
    path('customerorder',CustomerOrderView.as_view(),name='customerorder'),
    path('orders-view/<int:pk>',orderView.as_view(),name="ordersview"),
    path('customerorder',OrderListView.as_view(),name="orders"),
    path('addreview/<int:pk>',ReviewView.as_view(),name="addreview"),
    path('displayreview/<int:pk>',DisplayReView.as_view(),name="displayreview"),
    path('locationdonor/<int:pk>/', LocationView.as_view(), name="location"),
    path('logout/', LogoutView.as_view(), name='logout')
    
    
  


]