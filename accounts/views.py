from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *

from .forms import *
from .models import *

from django.core.mail import send_mail
import random
from WebApplication import settings
import time

# Create your views here.
@super_user
def home(request):
	return render(request, 'accounts/home.html')

class ClientSignUpView(CreateView):

	model = User
	form_class = ClientSignUpForm
	template_name = 'accounts/register.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'client'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		user.otp = random.randint(1000000, 9999999)
		user.save()
		sub = "Nykinsky One Time Password"
		message = "Hello " + user.first_name + "\n" + "Your OTP is " + str(user.otp)
		send_mail(sub, message, settings.EMAIL_HOST_USER, [user.email])
		login(self.request, user)
		return redirect('verify_email')
		

class PartnerSignUpView(CreateView):
	model = User
	form_class = PartnerSignUpForm
	template_name = 'accounts/register.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'partner'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		user.otp = random.randint(1000000, 9999999)
		user.save()
		sub = "Nykinsky One Time Password"
		message = "Hello " + user.first_name + "\n" + "Your OTP is " + str(user.otp)
		send_mail(sub, message, settings.EMAIL_HOST_USER, [user.email])
		login(self.request, user)
		return redirect('verify_email')

def ClientloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None and user.is_client:
			login(request, user)
			if user.email_verified:
				return redirect('client')
			else:
				user.otp = random.randint(1000000, 9999999)
				user.save()
				sub = "Nykinsky One Time Password"
				message = "Hello " + user.first_name + "\n" + "Your OTP is " + str(user.otp)
				send_mail(sub, message, settings.EMAIL_HOST_USER, [user.email])
				return redirect('verify_email')
		else:
			messages.info(request, 'Email-id or Password Incorrect')
	return render(request, 'accounts/login.html', {'user_type':'client'})

def PartnerloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None and user.is_partner:
			login(request, user)
			if user.email_verified:
				return redirect('partner')
			else:
				user.otp = random.randint(1000000, 9999999)
				user.save()
				sub = "Nykinsky One Time Password"
				message = "Hello " + user.first_name + "\n" + "Your OTP is " + str(user.otp)
				send_mail(sub, message, settings.EMAIL_HOST_USER, [user.email])
				return redirect('verify_email')
		else:
			messages.info(request, 'Email-id or Password Incorrect')
	return render(request, 'accounts/login.html', {'user_type':'partner'})

def ClientlogoutPage(request):
	logout(request)
	return redirect('client-login')

def PartnerlogoutPage(request):
	logout(request)
	return redirect('partner-login')

@partner_required
@profile_update_required
def partner(request):
	partner = Partner.objects.get(user = request.user)
	if partner.is_approved:
		sqlcommand1 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id NOT IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id ) AND partner_id = %s)'
		todo = Order.objects.raw(sqlcommand1,[partner.pk])
		sqlcommand2 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id ) AND partner_id = %s)'
		done = Order.objects.raw(sqlcommand2,[partner.pk])
		context = {'partner':partner, 'todo_no':len(todo), 'done_no':len(done)}
		return render(request, 'accounts/partner.html', context)
	else :
		return render(request,'accounts/temporary-partner.html')

@partner_required
def partnerpendingorders(request):
	partner = Partner.objects.get(user = request.user)
	if partner.is_approved:
		sqlcommand1 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id NOT IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id ) AND partner_id = %s)'
		todo = Order.objects.raw(sqlcommand1,[partner.pk])
		context = { 'todo': todo}
		return render(request, 'accounts/partner-pendingorders.html', context)
	else :
		return render(request,'accounts/temporary-partner.html')

@partner_required 
def partnerdeliveredorders(request):
	partner = Partner.objects.get(user = request.user)
	if partner.is_approved:
		sqlcommand2 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id ) AND partner_id = %s)'
		done = Order.objects.raw(sqlcommand2,[partner.pk])
		context = { 'done': done}
		return render(request, 'accounts/partner-deliveredorders.html', context)
	else :
		return render(request,'accounts/temporary-partner.html')

@partner_required
def partnerprofile(request):
	partner = Partner.objects.get(user = request.user)
	try :
		profile = Partnerprofile.objects.get(partner = partner) 
		form = partnerprofileform(instance = profile)
		if request.method == 'POST':
			form = partnerprofileform(request.POST,request.FILES,instance=profile)
			if form.is_valid():
				partnerprfl = form.save(commit=False)
				partnerprfl.partner = partner
				partnerprfl.save()
				messages.success(request, "Profile updated successfully for " + partner.user.get_full_name())
				return redirect('partner')
			else :
				messages.error(request, 'Only pdf or docx files can be uploaded in file fields and jpeg or png files can only be uploaded in image field')
	except :
		form = partnerprofileform()
		if request.method == 'POST':
			form = partnerprofileform(request.POST,request.FILES)
			if form.is_valid():
				partnerprfl = form.save(commit=False)
				partnerprfl.partner = partner
				partnerprfl.save()
				messages.success(request, "Profile updated successfully for " + partner.user.get_full_name())
				return redirect('partner')
			else :
				messages.error(request, 'Only pdf or docx files can be uploaded in file fields and jpeg or png files can only be uploaded in image field')
	context = {'form':form}
	return render(request, 'accounts/partner-profile.html', context)

@client_required
@profile_update_required
def client(request):
	client = Client.objects.get(user = request.user)
	my_orders = Order.objects.filter(client = client)
	sqlcommand2 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id )) AND client_id = %s'
	done = Order.objects.raw(sqlcommand2,[client.pk])
	context = {'client':client, 'orders': my_orders, 'done':done}
	return render(request, 'accounts/client.html', context)

@client_required
def clientorders(request):
	client = Client.objects.get(user = request.user)
	my_orders = Order.objects.filter(client = client)
	context = {'orders': my_orders}
	return render(request, 'accounts/client-orders.html', context)

@client_required
def clientdeliveredorders(request):
	client = Client.objects.get(user = request.user)
	sqlcommand2 = 'SELECT * from accounts_order where accounts_order.id IN ( Select order_id from accounts_manage where id IN ( SELECT accounts_manage.id from accounts_manage,accounts_product where accounts_manage.id=accounts_product.managed_id )) AND client_id = %s'
	done = Order.objects.raw(sqlcommand2,[client.pk])
	context = {'done':done}
	return render(request, 'accounts/client-deliveredorders.html', context)

@client_required
def clientprofile(request):
	client = Client.objects.get(user = request.user)
	try :
		profile = Clientprofile.objects.get(client = client) 
		form = clientprofileform(instance = profile)
		if request.method == 'POST':
			form = clientprofileform(request.POST,request.FILES,instance=profile)
			if form.is_valid():
				clientprfl = form.save(commit=False)
				clientprfl.client = client
				clientprfl.save()
				messages.success(request, "Profile updated successfully for " + client.user.get_full_name())
				return redirect('client')
			else :
				messages.error(request, 'Only pdf or docx files can be uploaded in file fields and jpeg or png files can only be uploaded in image field')
	except :
		form = clientprofileform()
		if request.method == 'POST':
			form = clientprofileform(request.POST,request.FILES)
			if form.is_valid():
				clientprfl = form.save(commit=False)
				clientprfl.client = client
				clientprfl.save()
				messages.success(request, "Profile updated successfully for " + client.user.get_full_name())
				return redirect('client')
			else :
				messages.error(request, 'Only pdf or docx files can be uploaded in file fields and jpeg or png files can only be uploaded in image field')
	context = {'form':form}
	return render(request, 'accounts/client-profile.html', context)



@client_required
def createOrder(request):
	form = CreateOrderForm()
	context = {'form':form}
	client = Client.objects.get(user = request.user)
	if request.method == 'POST':
		form = CreateOrderForm(request.POST, request.FILES)
		if form.is_valid():
			order = form.save(commit=False)
			order.client = client
			order.save()
			messages.success(request, "Order placed successfully for " + client.user.get_full_name())
			return redirect('client')
		else :
			messages.error(request, 'Only pdf or docx files can be uploaded')
	
	return render(request, 'accounts/create-order.html', context)

@client_required
def viewProduct(request,pk):
	client = Client.objects.get(user = request.user)
	order = Order.objects.get(id = pk)
	sqlcommand = 'SELECT * from accounts_product where managed_id IN (SELECT id from accounts_manage where accounts_manage.order_id = %s )'
	product = Order.objects.raw(sqlcommand,[pk])
	sqlcommand1 = 'SELECT * from accounts_manage where accounts_manage.order_id = %s '
	managed = Manage.objects.raw(sqlcommand1,[pk])
	context = {'client':client, 'order': order, 'product': product[0], 'partner': managed[0].partner}
	return render(request, 'accounts/view-product.html', context)

@partner_required
def viewpartnerProduct(request,pk):
	partner = Partner.objects.get(user = request.user)
	if partner.is_approved :
		order = Order.objects.get(id = pk)
		sqlcommand = 'SELECT * from accounts_product where managed_id IN (SELECT id from accounts_manage where accounts_manage.order_id = %s )'
		product = Order.objects.raw(sqlcommand,[pk])
		context = {'client':order.client, 'order': order, 'product': product[0], 'partner': partner}
		return render(request, 'accounts/view-product.html', context)
	else :
		return render(request,'accounts/temporary-partner.html')

@partner_required
def deliverProduct(request,pk):
	form = DeliverProductForm()
	partner = Partner.objects.get(user = request.user)
	if partner.is_approved :
		order = Order.objects.get(id = pk)
		managed = Manage.objects.get(order = order)
		context = {'form':form, 'order':order, 'partner':partner}

		if request.method == 'POST':

			form = DeliverProductForm(request.POST, request.FILES)
			if form.is_valid():
				product = form.save(commit=False)
				product.managed = managed
				product.save()

				messages.success(request, "Product delivered successfully to " + order.client.user.get_full_name())
			return redirect('partner')
	
		return render(request, 'accounts/review-order.html', context)
	else :
		return render(request,'accounts/temporary-partner.html')

def manager(request):
	if request.user is not None and request.user.is_staff:
		sqlcommand3 = 'SELECT * from accounts_order where accounts_order.id NOT IN ( Select order_id from accounts_manage)'
		sqlcommand4 = 'SELECT * from accounts_partner where (accounts_partner.user_id IN (SELECT accounts_user.id from accounts_user where accounts_user.email_verified IS TRUE)) AND accounts_partner.is_approved IS FALSE'
		sqlcommand5 =  'SELECT * from accounts_partner where (accounts_partner.user_id IN (SELECT accounts_user.id from accounts_user where accounts_user.email_verified IS TRUE)) AND accounts_partner.is_approved IS TRUE'
		ToBAsnd = Order.objects.raw(sqlcommand3)
		all_partners = Partner.objects.raw(sqlcommand4)
		actual_partners = Partner.objects.raw(sqlcommand5)
		context = {'ToBAsnd':ToBAsnd, 'partners':all_partners, 'actual_partners':actual_partners}
		return render(request, 'accounts/manager.html', context)
	else:
		return HttpResponse("<h3>Permission Denied</h3>")

def approvepartnerpage(request,pk):
	if request.user is not None and request.user.is_staff:
		user=User.objects.get(id=pk)
		partner = Partner.objects.get(user=user)
		context = {'partner':partner, 'services':partner.services_provided.all()}
		return render(request,'accounts/approve-partner.html',context)
	else:
		return HttpResponse("<h3>Permission Denied</h3>")

def approvepartner(request,pk):
	if request.user is not None and request.user.is_staff:
		user=User.objects.get(id=pk)
		partner = Partner.objects.get(user=user)
		partner.is_approved = True
		partner.save()
		return redirect('manager')
	else:
		return HttpResponse("<h3>Permission Denied</h3>")

def disapprovepartner(request,pk):
	if request.user is not None and request.user.is_staff:
		partner=User.objects.get(id=pk)
		partner.delete()
		return redirect('manager')
	else:
		return HttpResponse("<h3>Permission Denied</h3>")

def AssignPartner(request,pk):
	if request.user is not None and request.user.is_staff:
		order = Order.objects.get(id = pk)
		service = order.service_req
		filtered_partners = Partner.objects.filter(services_provided__in=[service.id])
		form = PartnerSelectForm()
		context = {'form':form,'filtered_partners':filtered_partners, 'order':order,}

		if request.method == 'POST':
			# print(request.POST['desired_partner'])
			form = PartnerSelectForm(request.POST)
			if form.is_valid():
				
				desired_partner = Partner.objects.get(pk = request.POST['desired_partner'])
				manage = form.save(commit=False)
				manage.partner = desired_partner
				manage.order = order
				manage.save()

				messages.success(request, "Partner assigned successfully to " + order.client.user.get_full_name())
			return redirect('manager')
		
		return render(request, 'accounts/assign-partner.html', context)
	else:
		return HttpResponse("<h3>Permission Denied</h3>")

@mailnotverified
def verify_email(request):
	user = request.user
	start = int(round(time.time()))
	if request.POST.get('send_new'):
		sub = "Nykinsky One Time Password"
		message = "Hello" + user.first_name + "\n" + "Your OTP is " + str(user.otp)
		send_mail(sub, message, settings.EMAIL_HOST_USER, [user.email])
		form = VerifyMailForm()
		return render(request, 'accounts/verify_mail.html', {'form':form})
	elif request.POST.get('verify'):
		if int(round(time.time())) - start <= 360:
			otp = int(request.POST.get('otp'))
			print(str(otp), str(user.otp))
			if otp == user.otp:
				user.email_verified = True
				user.save()
				if user.is_client:
					return redirect('client')
				else:
					return redirect('partner')
			else:
				logout(request)
				return render(request, 'accounts/wrong_otp.html')
		else:
			logout(request)
			return render(request, 'account/time_out.html')
	else:
		return render(request, 'accounts/verify_mail.html')
