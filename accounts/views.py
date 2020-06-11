from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from django.contrib import messages

from .forms import ClientSignUpForm, PartnerSignUpForm
from .models import *

# Create your views here.

def home(request):
	orders = Order.objects.all()
	clients = Client.objects.all()

	context = {'orders': orders, 'clients':clients}
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


def ClientloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		print(email)

		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Email-id or Password Incorrect')

	return render(request, 'accounts/login.html', {'user_type':'client'})

def PartnerloginPage(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		print(email)

		user = authenticate(request, email=email, password=password)
		print(user)
		if user is not None:
			login(request, user)
			return redirect('home')
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

def partner(request):
	return render(request, 'accounts/products.html')

def client(request):
	return render(request, 'accounts/customer.html')

