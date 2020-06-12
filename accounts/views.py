from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *

from .forms import ClientSignUpForm, PartnerSignUpForm, CreateOrderForm
from .models import *

# Create your views here.
@login_required(login_url='client-login')
def home(request):
	orders = Order.objects.all()
	clients = Client.objects.all()
	total_orders_count = orders.count()
	delivered_orders = Manage.objects.values('order_id')
	# print(delivered_orders[0])
	pending_orders = []
	for order in orders:
		if order.id in delivered_orders:
			print(order.id)

	context = {'orders': orders, 'clients':clients, 'total_orders':total_orders_count}
	return render(request, 'accounts/dashboard.html',context)

class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('client-login')

class PartnerSignUpView(CreateView):
    model = User
    form_class = PartnerSignUpForm
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'partner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('partner-login')

@unauthenticated_user
def ClientloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None and user.is_client:
			login(request, user)
			return redirect('client')
		else:
			messages.info(request, 'Email-id or Password Incorrect')
	return render(request, 'accounts/login.html', {'user_type':'client'})

@unauthenticated_user
def PartnerloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None and user.is_partner:
			login(request, user)
			return redirect('partner')
		else:
			messages.info(request, 'Email-id or Password Incorrect')
	return render(request, 'accounts/login.html', {'user_type':'partner'})

def ClientlogoutPage(request):
	logout(request)
	return redirect('client-login')

def PartnerlogoutPage(request):
	logout(request)
	return redirect('partner-login')

# def registerPage(request):
# 	form = ClientForm()

# 	if request.method == 'POST':
# 		form = ClientForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			user = form.cleaned_data.get('firstname')
# 			messages.success(request, "Account is created for " + user)
# 			print(form)
# 			return redirect('login')
# 		else:
# 			return HttpResponse("404 error")
		
# 	context = {'form':form}
# 	return render(request, 'accounts/register.html', context)

@partner_required
def partner(request):
	return render(request, 'accounts/products.html')

@client_required
def client(request):
	client = Client.objects.get(user = request.user)
	print(client)
	my_orders = Order.objects.filter(client = client)
	context = {'client':client, 'orders': my_orders}
	return render(request, 'accounts/customer.html', context)

@client_required
def createOrder(request):
	form = CreateOrderForm()
	context = {'form':form}
	client = Client.objects.get(user = request.user)

	if request.method == 'POST':
		print(f"print post: {request.POST}")

		form = CreateOrderForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			order.client = client
			order.save()

			messages.success(request, "Order added successfully for " + client.user.get_full_name())
		return redirect('client')
	
	return render(request, 'accounts/create-order.html', context)

