from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,SetPasswordForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash


# Signup view function
def sign_up(request):
    if request.method == "POST":
      fm = SignUpForm(request.POST)
      if fm.is_valid():
        messages.success(request, 'Account Created Successfully !!')
        fm.save()
    else:    
      fm=SignUpForm()
    return render(request, 'enroll/signup.html',{'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            fm= AuthenticationForm( request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    #return HttpResponseRedirect('/profile/')
                    return render(request, 'core/home.html')
        else:            
            fm=AuthenticationForm()
        return render(request, 'enroll/userlogin.html',{'form':fm})
    else:
        #return HttpResponseRedirect('/profile/') 
        return render(request, 'core/home.html')


# to show login screen even if user is login by typing login in the url bar.
#def user_login(request):
    #if request.method =="POST":
        #fm= AuthenticationForm( request=request, data=request.POST)
        #if fm.is_valid():
            #uname = fm.cleaned_data['username']
            #upass = fm.cleaned_data['password']
            #user = authenticate(username=uname,password=upass)
            #if user is not None:
                #login(request, user)
                #messages.success(request, 'Logged in successfully !!')
                #return HttpResponseRedirect('/profile/')
    #else:            
        #fm=AuthenticationForm()
    #return render(request, 'enroll/userlogin.html',{'form':fm})

#profile
def user_profile(request):
    if request.user.is_authenticated:  #this line  will check if user is authenticated only the user will be able to see the dashboard
      return render(request, 'enroll/profile.html', {'name': request.user})
    else:
      return HttpResponseRedirect('/login/')


# below profile for other user to se directly website without login
#def user_profile(request):
    #return render(request, 'enroll/profile.html', {'name': request.user})
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

# reset password with old password
#def user_change_pass(request):
#    if request.user.is_authenticated:
#        if request.method == "POST":
#            fm = PasswordChangeForm(user= request.user, data= request.POST)
#            if fm.is_valid():
#                fm.save()
#                update_session_auth_hash(request, fm.user)
#                messages.success(request,"Password changed succesfully")
#                return HttpResponseRedirect('/profile/')
#        else:
#            fm = PasswordChangeForm(user= request.user)
#        return render(request, 'enroll/changepass.html',{'form':fm})
#    else:
#        return HttpResponseRedirect('/login/')



# reset password without old password
def user_change_pass1(request):
    #if request.user.is_authenticated:
    if request.user:
        if request.method == "POST":
            fm = SetPasswordForm(user= request.user, data= request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,"Password changed succesfully")
                return render(request, 'enroll/login.html',{'form':fm})
                #return HttpResponseRedirect('/profile/')
        else:
            fm = SetPasswordForm(user= request.user)
        return render(request, 'enroll/changepass1.html',{'form':fm})
    else:
        return HttpResponseRedirect('/changepass1/')


def admin_profile(request):
    if request.user.is_superuser == True:
     return HttpResponseRedirect('/home/')
    
        