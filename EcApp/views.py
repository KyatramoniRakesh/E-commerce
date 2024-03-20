from django.shortcuts import render
from django.views import View
from .models import Product
from django.db.models import Count
# Create your views here.
def home(request):
    return render(request,'home.html')

class Category(View):
    def get(self,request,val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title').annotate(total=Count('title'))
        return render(request,'category.html',locals())