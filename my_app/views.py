from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.cache import never_cache
from django.views import View
from django.utils.decorators import method_decorator
from .models import Domain, Module, TestCase
# from django import csrf_protect
from django.views.decorators.csrf import csrf_protect  # Add this import

# Home page with login functionality
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, 'home.html')

# Homepage view, displaying domains
@never_cache
@login_required
def homepage(request):
    domains = Domain.objects.all()
    return render(request, "homepage.html", {'domains': domains})

# Fetch modules for a given domain via Ajax
@never_cache
@login_required
def get_modules(request):
    domain_id = request.GET.get('domain_id')
    modules = Module.objects.filter(domain_id=domain_id).values('id', 'name') if domain_id else []
    return JsonResponse(list(modules), safe=False)

# Display test cases for a specific domain and module
@never_cache
@login_required
def test_case_view(request, domain_id, module_id):
    # Ensure that valid domain_id and module_id are passed in the URL
    try:
        test_cases = TestCase.objects.filter(module__domain_id=domain_id, module_id=module_id)
    except TestCase.DoesNotExist:
        test_cases = []  # Return an empty list if no test cases are found

    return render(request, "test_case_template.html", {"test_cases": test_cases})

# User registration view
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

# Logout view
class LogoutView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        logout(request)  # Logs out the user
        request.session.flush()  # Clears the session
        return redirect('home')  # Redirect after logout

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])

# Add domain functionality
@never_cache
@login_required
def add_domain(request):
    if request.method == "POST":
        domain_name = request.POST.get("domain_name").strip()
        if Domain.objects.filter(name__iexact=domain_name).exists():
            messages.error(request, "Domain already exists.")
        else:
            Domain.objects.create(name=domain_name)
            messages.success(request, "Domain added successfully.")
    return redirect('homepage')

# Add module functionality
@never_cache
@login_required
def add_module(request):
    if request.method == "POST":
        domain_id = request.POST.get("domain_id")
        module_name = request.POST.get("module_name").strip()

        if Module.objects.filter(name__iexact=module_name, domain_id=domain_id).exists():
            messages.error(request, "Module already exists for the selected domain.")
        else:
            Module.objects.create(name=module_name, domain_id=domain_id)
            messages.success(request, "Module added successfully.")
    return redirect('homepage')

# Test case dashboard with filtering by domain and module
@never_cache
@login_required
def test_case_dashboard(request):
    domain_id = request.GET.get('domain_id')
    module_id = request.GET.get('module_id')

    test_cases = TestCase.objects.all()

    if domain_id:
        test_cases = test_cases.filter(module__domain_id=domain_id)

    if module_id:
        test_cases = test_cases.filter(module_id=module_id)

    domains = Domain.objects.all()  # Fetch all domains

    return render(request, 'test_case_dashboard.html', {
        'test_cases': test_cases,
        'domains': domains
    })

# Edit test case functionality
@never_cache
@login_required
def edit_test_case(request, test_case_id):
    test_case = get_object_or_404(TestCase, id=test_case_id)
    if request.method == "POST":
        test_case.name = request.POST['name']
        test_case.description = request.POST['description']
        test_case.save()
        return redirect('test_case_dashboard')
    return render(request, 'edit_test_case.html', {'test_case': test_case})

# Delete test case functionality
@never_cache
@login_required
def delete_test_case(request, test_case_id):
    test_case = get_object_or_404(TestCase, id=test_case_id)
    test_case.delete()
    return redirect('test_case_dashboard')
@never_cache
@login_required
def add_test_case(request):
    if request.method == "POST":
        module_id = request.POST.get("module")
        name = request.POST.get("name")
        description = request.POST.get("description")

        module = Module.objects.get(id=module_id)
        TestCase.objects.create(module=module, name=name, description=description)

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False}, status=400)
@never_cache
@login_required
def test_case_list(request):
    test_cases = TestCase.objects.all()
    domains = Domain.objects.all()

    selected_domain_id = request.GET.get("domain", "")
    selected_module_id = request.GET.get("module", "")

    modules = Module.objects.none()
    if selected_domain_id:
        modules = Module.objects.filter(domain_id=selected_domain_id)
        test_cases = test_cases.filter(module__domain_id=selected_domain_id)
    if selected_module_id:
        test_cases = test_cases.filter(module_id=selected_module_id)

    return render(
        request,
        "test_case_list.html",
        {
            "test_cases": test_cases,
            "domains": domains,
            "modules": modules,
            "selected_domain_id": selected_domain_id,
            "selected_module_id": selected_module_id,
        },
    )
