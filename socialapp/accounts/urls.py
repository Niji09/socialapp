from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as account_views


app_name = 'accounts'
urlpatterns = [
	path('signup/', account_views.UserSignUpView.as_view(), name='signup'),
	path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', account_views.change_password, name='change_password'),
]