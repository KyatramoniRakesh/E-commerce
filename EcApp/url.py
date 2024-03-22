from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path
from . import views
from .forms import Login,MyPasswordChangeForm

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('category/<slug:val>', views.Category.as_view(),name='category'),
    path('product_details/<int:pk>', views.Product_Details.as_view(), name='productdetails'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('updateaddress/<int:pk>',views.UpdateAddress.as_view(),name='update_add'),

    #login authentication
    path('registration',views.CustomerRegistration.as_view(),name='registration'),
    path('accounts/login',auth_view.LoginView.as_view(template_name = 'Login.html',authentication_form = Login), name='login'),
    path('passwordchange',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',
                form_class = MyPasswordChangeForm,success_url='changepassworddone.html'),name='pc'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='changepassworddone.html'),name='passwordchangedone'),

    # path('password_change/',auth_view.PasswordChangeView.as_view(template_name = 'Password_reset.html'),form_class=PasswordReset,
    #                                                            name='password_reset')


    ]+static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
