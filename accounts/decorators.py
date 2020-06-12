from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def client_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='client-login'):
    '''
    Decorator for views that checks that the logged in user is a client,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_client,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def partner_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='partner-login'):
    '''
    Decorator for views that checks that the logged in user is a partner,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_partner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_client:
                return redirect('client')
            elif request.user.is_partner:
                return redirect('partner')
            else:
                return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func