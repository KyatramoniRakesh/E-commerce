from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('category/<slug:val>', views.Category.as_view(),name='category'),
    path('product_details/<int:pk>', views.Product_Details.as_view(), name='productdetails'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),

    #login authentication
    path('registration',views.CustomerRegistration.as_view(),name='registration')
]+static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
