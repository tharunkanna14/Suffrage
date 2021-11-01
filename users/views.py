from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegisterForm, LoginForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import time
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            subject = "Welcome to Suffrage"
            message = f'Hi {user.username},Thank You for registering in our platform.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            

            send_mail( subject, message, email_from, recipient_list )
   

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )

            login(request, new_user)
            return redirect('index')
        else:
            messages.warning(request,'Oops! some error occured, try agin.')
    
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html',{'form':form})

@login_required
def user_logout(request):
    time.sleep(2) # waiting for 2 sec
    logout(request) # using django.contrib.auth.logout(), It takes an HttpRequest object and has no return value
    messages.success(request,f'You are logged out successfully') # logout success msg
    return redirect('login') # redirect to login page