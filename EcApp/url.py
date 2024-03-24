from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path
from . import views
from .forms import Login,MyPasswordChangeForm,MySetPasswordForm,MyPasswordResetForm

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('category/<slug:val>', views.Category.as_view(),name='category'),
    path('product_details/<int:pk>', views.Product_Details.as_view(), name='productdetails'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('updateaddress/<int:pk>',views.UpdateAddress.as_view(),name='update_add'),

    #Add_to_cart
    path('add',views.add_to_cart, name='add'),
    path('cart',views.show_cart, name='cart'),
    path('checkout',views.Checkout.as_view(), name='checkout'),

    path('pluscart',views.plus_cart),
    path('minuscart',views.minus_cart),
    path('removecart', views.remove_cart),


    #login authentication
    path('registration',views.CustomerRegistration.as_view(),name='registration'),
    path('accounts/login',auth_view.LoginView.as_view(template_name = 'Login.html',authentication_form = Login), name='login'),
    path('passwordchangedone',auth_view.PasswordChangeDoneView.as_view(template_name='changepassworddone.html'),name='passwordchangedone'),
    path('passwordchange',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',
                form_class = MyPasswordChangeForm,success_url='passwordchangedone'),name='pc'),
    path('logout',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',
    form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html') ,
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',
                                            form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    ]+static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)
