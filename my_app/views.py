from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .models import Domain, Module, TestCase
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseNotAllowed
from django.views import View

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
    domains = Domain.objects.all()
    return render(request, "homepage.html", {'domains': domains})
@never_cache
@login_required
def get_modules(request):
    domain_id = request.GET.get('domain_id')
    modules = Module.objects.filter(domain_id=domain_id).values('id', 'name')
    return JsonResponse(list(modules), safe=False)

@never_cache
@login_required
def test_case_view(request, domain_id, module_id):
    test_case = TestCase.objects.filter(domain_id=domain_id, module_id=module_id).first()
    return render(request, 'test_case_template.html', {'test_case': test_case})

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

class LogoutView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        logout(request)  # Logs out the user
        request.session.flush()  # Clears the session
        return redirect('home')  # Redirect after logout

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])


@never_cache
@login_required
def add_domain(request):
    if request.method == "POST":
        domain_name = request.POST.get('domain_name')
        if domain_name:
            Domain.objects.create(name=domain_name)
    return redirect('homepage')
@never_cache
@login_required
def add_module(request):
    if request.method == "POST":
        domain_id = request.POST.get('domain_id')
        module_name = request.POST.get('module_name')
        if domain_id and module_name:
            domain = Domain.objects.get(id=domain_id)
            Module.objects.create(domain=domain, name=module_name)
    return redirect('homepage')



     