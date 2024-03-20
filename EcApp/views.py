from django.shortcuts import render
from django.views import View
from .models import Product
from django.db.models import Count
from .forms import Registration
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