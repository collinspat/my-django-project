from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # checks who the user is so that it can decide what they are allowed to see 
        if user.is_authenticated:
            if user.user_type == '1':  # Administrator 
                if modulename == 'voting.views':
                    error = True
                    if request.path == reverse('fetch_ballot'):
                        pass
                    else:
                        messages.error(
                            request, "You do not have access to this resource")
                        return redirect(reverse('adminDashboard'))
            elif user.user_type == '2':  # Voter
                if modulename == 'administrator.views':
                    messages.error(
                        request, "You do not have access to this resource")
                    return redirect(reverse('voterDashboard'))
            else:  #if you are not a voter or admin it means you first need to register at the login page 
                return redirect(reverse('account_login'))
        else:
            
            if request.path == reverse('account_login') or request.path == reverse('account_register') or modulename == 'django.contrib.auth.views' or request.path == reverse('account_login'):
                pass
            elif modulename == 'administrator.views' or modulename == 'voting.views':
                # If visitor tries to access administrator or voters functions
                messages.error(
                    request, "You need to be logged in to perform this operation")
                return redirect(reverse('account_login'))
            else:
                return redirect(reverse('account_login'))
