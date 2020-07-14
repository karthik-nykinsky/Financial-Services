from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.db import transaction
import re
from .database import *

class ClientSignUpForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    phone = forms.CharField(max_length=100)
    company = forms.CharField(max_length=200)
    designation = forms.CharField(label='Your Designation in company?', widget=forms.Select(choices=AUTHORIZED_PERSON_POSITION))
    mobile = forms.CharField(max_length=10)
    address = forms.CharField(max_length=500)
    state = forms.CharField(max_length=150)
    city = forms.CharField(max_length=100)
    pin = forms.CharField(max_length=10)
    company_type = forms.CharField(widget=forms.Select(choices=TYPE_OF_COMPANY))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_client = True
        user.save()
        phone = self.cleaned_data.get('phone')
        company = self.cleaned_data.get('company')
        mobile = self.cleaned_data.get('mobile')
        des = self.cleaned_data.get('designation')
        add = self.cleaned_data.get('address')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        pin = self.cleaned_data.get('pin')
        toc = self.cleaned_data.get('company_type')
        client = Client.objects.create(user=user, company_type = toc, phone=phone, company = company,designation = des,mobile =mobile,address =add,state = state,city = city,pin = pin)
        return user


class PartnerSignUpForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )
    services_provided = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    address = forms.CharField(max_length=500)
    state = forms.CharField(max_length=150)
    city = forms.CharField(max_length=100)
    pin = forms.CharField(max_length=10)
    work_exp = forms.IntegerField(min_value=0)
    ca_final = forms.ChoiceField(choices = BOOL_CHOICES, initial='', widget=forms.Select(), required=True)
    cfa_level3 =forms.ChoiceField(choices = BOOL_CHOICES, initial='', widget=forms.Select(), required=True)
    ifc = forms.ChoiceField(choices = BOOL_CHOICES, initial='', widget=forms.Select(), required=True)
    frm_acc =forms.ChoiceField(choices = BOOL_CHOICES, initial='', widget=forms.Select(), required=True)
    previous_work = forms.CharField(required=False,max_length=1000)
    phone = forms.CharField(max_length=12)
    resume = forms.FileField(max_length=100, required=True)
    company = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_partner = True
        user.save()
        partner = Partner.objects.create(user=user,
                 address=self.cleaned_data.get('address'),
                 state = self.cleaned_data.get('state'),
                 city = self.cleaned_data.get('city'),
                 pin = self.cleaned_data.get('pin'),
                 ca_final = self.cleaned_data.get('ca_final'),
                 cfa_level3 = self.cleaned_data.get('cfa_level3'),
                 ifc = self.cleaned_data.get('ifc'),
                 frm_acc = self.cleaned_data.get('frm_acc'),
                 work_exp = self.cleaned_data.get('work_exp'),
                 previous_work = self.cleaned_data.get('previous_work'),
                 phone = self.cleaned_data.get('phone'),
                 resume = self.cleaned_data.get('resume'),
                 company = self.cleaned_data.get('company'))
        partner.services_provided.add(*self.cleaned_data.get('services_provided'))
        return user


class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['service_req', 'city', 'comments', 'documents']


class DeliverProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['comments', 'documents']


class PartnerSelectForm(forms.ModelForm):

    class Meta:
        model = Manage
        fields = []


class clientprofileform(forms.ModelForm):

    class Meta:
        model = Clientprofile
        fields = ['logo','Official_photo','Aadhar_card','Pan_card','Certificate_of_Inc','Company_Pan_card','Payment_slip','TAN_Document']


class partnerprofileform(forms.ModelForm):

    class Meta:
        model = Partnerprofile
        fields = ['Official_photo','Aadhar_card','Pan_card','Work_experience','Payment_slip','Educational_certificate']