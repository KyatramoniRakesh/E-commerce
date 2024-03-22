from django.shortcuts import render,redirect
from django.views import View
from .models import Product
from django.db.models import Count
from .forms import Registration,CustomerProfileForm
from django.contrib import messages
from .models import Customer

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')

class Category(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title').annotate(total=Count('title'))
        return render(request,'category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request,'category.html',locals())

class Product_Details(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'ProductDetails.html',{'product': product})

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

class Profile(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',{'form': form})
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
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

class UpdateAddress(View):
    def get(self,request,pk):
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

