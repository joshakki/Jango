from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username ,password=password)

        if user is not None:
            login(request,user)
            return redirect("homepage")
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request, 'home.html')

@never_cache
@login_required
def homepage(request):
    return render(request, "homepage.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect("home")  # Redirect after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('')


     