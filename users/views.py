from django.shortcuts import render, redirect
from .forms import LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout


class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            print("[LOGGER] Authenticating user")
            if user is not None:
                login(request,user)
                print("[LOGGER] Logged in")
                if user.role == 'creditor':
                    return redirect('home')
                elif user.role == 'accountant':
                    return redirect('accounting:home')
                else:
                    return redirect('home')
            else:
                print("[LOGGER] Error in loggin in")
                return redirect('auth:login')
        return render(request,"login.html",{"form":form})



def logoutview(request):
    logout(request)
    return redirect("home")