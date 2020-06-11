from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/client', views.ClientloginPage, name='client-login'),
    path('login/partner', views.PartnerloginPage, name='partner-login'),
    path('logout/client', views.ClientlogoutPage, name='client-logout'),
    path('logout/partner', views.PartnerlogoutPage, name='partner-logout'),
    path('register/client', views.ClientSignUpView.as_view(), name='client-register'),
    path('register/partner', views.PartnerSignUpView.as_view(), name='partner-register'),
    path('partner/', views.partner, name='partner'),
    path('client/', views.client, name='client'),
]