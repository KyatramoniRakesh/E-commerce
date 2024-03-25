import razorpay
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import Registration, CustomerProfileForm
from .models import Product, Cart, Payment,Customer,OrderPlaced
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.
def home(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'home.html',locals())
def about(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'about.html',locals())
def contact(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    return render(request,'contact.html',locals())

class Category(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        title = Product.objects.filter(category = val).values('title').annotate(total=Count('title'))
        return render(request,'category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request,'category.html',locals())

class Product_Details(View):
    def get(self,request,pk):
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        return render(request,'ProductDetails.html',locals())

class CustomerRegistration(View):
    def get(self,request):
        form = Registration()
        return render(request,'registration.html',locals())
    def post(self,request):
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User registration successfully")
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'registration.html',locals())

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                auth_login(request, user)
                # Redirect the user to the URL specified in the 'next' parameter if it exists
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    # Redirect to a default URL after successful login
                    return redirect('home')  # Change 'home' to your desired URL name
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class Profile(View):
    def get(self,request):
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile created successfully")
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request, 'profile.html',locals())

def address(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")

def add_to_cart(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("cart",locals())
def show_cart(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
        totalamount = amount + 40
    return render(request,'addtocart.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount
            }
        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))
        return JsonResponse(data)


class Checkout(View):
    def get(self,request):

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client =  razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount, "currency":"INR", "receipt":"ordered_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']

        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        totalitems = 0
        if request.user.is_authenticated:
            totalitems = len(Cart.objects.filter(user=request.user))

        return render(request,'checkout.html',locals())


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    print("payment done : oid=",order_id,'pid=',payment_id,'Cust id = ',cust_id)
    user = request.user
    customer = Customer.objects.get(id=cust_id)

    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart_items = Cart.objects.filter(user=user)
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity,
            payment=payment
        )
        cart_item.delete()
    return redirect('orders')


@login_required
def Orders(request):
    totalitems = 0
    if request.user.is_authenticated:
        totalitems = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', locals())