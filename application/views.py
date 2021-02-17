from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json

# main page function
def main(request):
    return render(request,'main.html')

def index(request):
    context = {}
    # if not request.user.is_authenticated:
    #     return redirect("login")
    if request.method == "POST":
        n = int(request.POST.get("n"))
        k = int(request.POST.get("k"))
        d = int(request.POST.get("d"))
        q = int(request.POST.get("q"))
        if "form-steps" in request.POST:
            form_step = request.POST.get("form-steps")
            if form_step and form_step != "":   
                if form_step == "specifying-parameters":
                    context['response'] = {
                        "n": n,
                        "k": k,
                        "d": d,
                        "q": q,
                        "sum": n + k + d + q
                    }

    return render(request, 'main.html', context)

# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

