from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('login/client', views.ClientloginPage, name='client-login'),
    path('login/partner', views.PartnerloginPage, name='partner-login'),
    path('logout/client', views.ClientlogoutPage, name='client-logout'),
    path('submit/client/', views.submit_client, name='client-submit'),
    path('submit/partner/', views.submit_partner, name='partner-submit'),
    path('logout/partner', views.PartnerlogoutPage, name='partner-logout'),
    path('register/client', views.ClientSignUpView.as_view(), name='client-register'),
    path('register/partner', views.PartnerSignUpView.as_view(), name='partner-register'),
    path('partner/', views.partner, name='partner'),
    path('client/', views.client, name='client'),
    path('client/create_order', views.createOrder, name='client-order'),
    path('client/view_product/<str:pk>/', views.viewProduct, name='view-product'),
    path('partner/view_product/<str:pk>/', views.viewpartnerProduct, name='partnerview-product'),
    path('partner/review_order/<str:pk>/', views.deliverProduct, name='deliver-product'),
    path('partner-profile/',views.partnerprofile, name= 'partner-profile'),
    path('verify_email/', views.verify_email, name= 'verify_email'),
    path('partner/partner-pendingorders/',views.partnerpendingorders, name= 'partner-pendingorders'),
    path('partner/partner-deliveredorders/',views.partnerdeliveredorders, name= 'partner-deliveredorders'),
    path('client/client-orders/',views.clientorders, name= 'client-orders'),
    path('client-profile/',views.clientprofile, name= 'client-profile'),
    path('client/client-deliveredorders/',views.clientdeliveredorders, name= 'client-deliveredorders'),
    path('manager/', views.manager, name='manager'),
    path('manager/manager-assignpartner/',views.managerassignpartner, name='manager-assignpartner'),
    path('manager/manager-assignpartner/assign_partner/<str:pk>/', views.AssignPartner, name='Assign-Partner'),
    path('manager/manager-approvepartner/', views.managerapprovepartner, name='manager-approvepartner'),
    path('manager/manager-approvepartner/approve_partner_page/<str:pk>/',views.approvepartnerpage, name='Approve-Partner-Page'),
    path('manager/manager-approvepartner/approve_partner_page/disapprove_partner/<str:pk>/',views.disapprovepartner, name='Disapprove-Partner'),
    path('manager/manager-approvepartner/approve_partner_page/approve_partner/<str:pk>/',views.approvepartner, name='Approve-Partner'),
    path('manager/manager-approvedpartners/',views.managerapprovedpartners, name='manager-approvedpartners'),
    path('manager/manager-approvedpartners/dismiss_partner/<str:pk>/',views.disapprovepartner, name='Dismiss-Partner'),
    path('manager/manager-viewclients/',views.managerviewclients, name='manager-viewclients'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)