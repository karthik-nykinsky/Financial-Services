from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



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
    path('client/create_order', views.createOrder, name='client-order'),
    path('client/view_product/<str:pk>/', views.viewProduct, name='view-product'),
    path('partner/view_product/<str:pk>/', views.viewpartnerProduct, name='partnerview-product'),
    path('partner/review_order/<str:pk>/', views.deliverProduct, name='deliver-product'),
    path('manager/assign_partner/<str:pk>/', views.AssignPartner, name='Assign-Partner'),
    path('manager/', views.manager, name='manager'),
    path('verify_email/', views.verify_email, name= 'verify_email'),
    path('partner-pendingorders/',views.partnerpendingorders, name= 'partner-pendingorders'),
    path('partner-deliveredorders/',views.partnerdeliveredorders, name= 'partner-deliveredorders'),
    path('client-orders/',views.clientorders, name= 'client-orders'),
    path('client-deliveredorders/',views.clientdeliveredorders, name= 'client-deliveredorders'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)