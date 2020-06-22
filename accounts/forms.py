from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.db import transaction


class ClientSignUpForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    phone = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_client = True
        user.save()
        client = Client.objects.create(user=user, phone=self.cleaned_data.get('phone'))
        print(self.cleaned_data.get('phone'))
        return user



class PartnerSignUpForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    company = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)

    services_provided = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'company', 'city')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_partner = True
        user.save()
        partner = Partner.objects.create(user=user, 
                company=self.cleaned_data.get('company') , 
                city=self.cleaned_data.get('city') )
        partner.services_provided.add(*self.cleaned_data.get('services_provided'))
        return user

class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['service_req', 'city', 'comments']

class DeliverProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['comments']

class PartnerSelectForm(forms.ModelForm):

    class Meta:
        model = Manage
        fields = ['partner']