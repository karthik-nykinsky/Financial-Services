from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .database import *

class UserManager(BaseUserManager):
    def create_user(
            self, email, first_name, last_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_client = False
        user.is_partner = False
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_client = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Service(models.Model):
    name = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.name 

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    company_type = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)

    def __str__(self):
        return self.user.get_full_name()

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf','.doc','.docx']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported!')

class Clientprofile(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    logo = models.ImageField(upload_to=client_logo,max_length=200)
    Official_photo = models.ImageField(upload_to=client_photo,max_length=200)
    Aadhar_card = models.FileField(upload_to=client_aadhar,max_length=200,validators=[validate_file_extension])
    Pan_card = models.FileField(upload_to=client_pan,max_length=200,validators=[validate_file_extension])
    Certificate_of_Inc = models.FileField(upload_to=client_coinc,max_length=200,validators=[validate_file_extension])
    Company_Pan_card = models.FileField(upload_to=client_cpan,max_length=200,validators=[validate_file_extension])
    Payment_slip = models.FileField(upload_to=client_ps,max_length=200,validators=[validate_file_extension])
    TAN_Document = models.FileField(upload_to=client_tan,max_length=200,validators=[validate_file_extension])

class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    services_provided = models.ManyToManyField(Service)
    ca_final = models.BooleanField()
    cfa_level3 = models.BooleanField()
    ifc = models.BooleanField()
    frm_acc = models.BooleanField()
    work_exp = models.IntegerField()
    previous_work = models.CharField(max_length=1000,null=True)
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)
    resume = models.FileField(max_length=100, upload_to=partner_resume, null=True)

    def __str__(self):
        return (self.user.first_name + ' '+self.user.last_name)

class Partnerprofile(models.Model):
    partner = models.ForeignKey(Partner, null=True, on_delete=models.SET_NULL)
    Official_photo = models.ImageField(upload_to=partner_photo)
    Aadhar_card = models.FileField(upload_to=partner_aadhar,max_length=200,validators=[validate_file_extension])
    Pan_card = models.FileField(upload_to=partner_pan,max_length=200,validators=[validate_file_extension])
    Work_experience = models.FileField(upload_to=partner_worexp,max_length=200,validators=[validate_file_extension])
    Payment_slip = models.FileField(upload_to=partner_ps,max_length=200,validators=[validate_file_extension])
    Educational_certificate = models.FileField(upload_to=partner_ec,max_length=200,validators=[validate_file_extension])


class Order(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    service_req = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=200, blank=False)
    documents = models.FileField(upload_to=order,max_length=200,validators=[validate_file_extension])
    comments = models.CharField(max_length=200, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)

class Manage(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    partner = models.ForeignKey(Partner, null=True, on_delete=models.SET_NULL)

class Product(models.Model):
    managed = models.ForeignKey(Manage, null=True, on_delete=models.SET_NULL)
    documents = models.FileField(upload_to=product,max_length=200,validators=[validate_file_extension])
    comments = models.CharField(max_length=200, null=True, blank=True)
