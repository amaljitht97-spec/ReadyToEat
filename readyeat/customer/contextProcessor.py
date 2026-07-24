from customer.models import *

def cartCount(request):
    if request.user.is_authenticated:
        customer=Customer.objects.filter(user=request.user).first()
        count=CartModel.objects.filter(customer=customer).count()
        return {"cartCount":count}
    return {"cartCount":0}