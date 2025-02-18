from django.urls import path
from .views import home ,homepage, register
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import get_modules, test_case_view, add_domain, add_module

urlpatterns = [
    path("", home , name ='home'),
    path("homepage/", homepage, name="homepage"),
    path("register/", register, name="register"),
    path("",  LogoutView.as_view(next_page=""), name="logout"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('get-modules/', get_modules, name='get_modules'),
    path('<int:domain_id>/<int:module_id>/', test_case_view, name='test_case'),
    path('add-domain/', add_domain, name='add_domain'),
    path('add-module/', add_module, name='add_module'),



]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])