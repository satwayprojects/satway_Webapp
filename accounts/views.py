from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
######################################
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
######################################

# Since using Custom User Model
# define User with the Custom User model, 
# you can do this with get_user_model at the top of the file  
# where you use User 
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

#User Login

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #print(username, password)
        try:
            user_exist = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Error: incorrect credentials")
            return render(request,'index/login.html')
            # context = {'status': 'User does not exist'}
            # return render(request, 'index/login.html', context)
        # Authenticating User
        if user_exist:        
            user = authenticate(request, username=username, password=password)
            print("User =", user)
            
            # Redirecting to respective user Dashboard
            if user is not None:
                login(request,user)
                #print("User Type = ",user.user_type)
                if user.user_type == 'US':
                    # app_name: in urls.py of app and view name
                    return HttpResponseRedirect(reverse('user:Dashboard'))
                elif user.user_type == 'SU':
                    return HttpResponseRedirect(reverse('subuser:Dashboard'))
                elif user.user_type == 'DI':
                    return HttpResponseRedirect(reverse('distributer:Dashboard'))
                elif user.user_type == 'AD':
                    return HttpResponseRedirect(reverse('master:Dashboard'))
                elif user.user_type == 'DE':
                    return HttpResponseRedirect(reverse('dealer:Dashboard'))
                elif user.user_type == 'SD':
                    return HttpResponseRedirect(reverse('subdealer:Dashboard'))
            else:
                # incorrect password
                messages.error(request, "Error: incorrect credentials")
                return render(request,'index/login.html')
    return render(request, 'index/login.html') 
        

#change Password section

def resetPassword(request):
    info = "" 
    context = {'message':info}
    if request.method == 'POST':
        username = request.POST.get('username')
        newPassword = request.POST.get('password')
        mobile = request.POST.get('mobile')
        for key, value in request.POST.items():
            print("Key = {} Value = {}".format(key,value))

        try:
            user_exist = User.objects.get(username=username,phone=mobile)
        except User.DoesNotExist:
            info = "User credentials incorrect"
            context = {'message':info}    
            return render(request, 'accounts/forgotpassword.html',context)

        if user_exist:
            print("Congrats")
            user_exist.set_password(newPassword)
            user_exist.save()
            return HttpResponseRedirect(reverse('index:loginPage'))
    else:
        info = "User credentials incorrect"
        context = {'message':info}
        return render(request, 'accounts/forgotpassword.html')
    
    context = {'message':info}    
    return render(request, 'accounts/forgotpassword.html',context)


#User Logout
@login_required
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('index:loginPage'))


@login_required
def viewProfile(request):
    currentuser = request.user
    username = currentuser.username

    user = User.objects.get(username=username)

    context = {'user': user}   
    return render(request, 'accounts/profile.html', context)


@login_required
def changePassword(request):

    if request.method == 'POST':
        # for key,value in request.POST.items():
        #     print(key, value)
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            u = request.user.user_type
            print(u)
            return redirect("/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/newpassword.html', {'form': form})