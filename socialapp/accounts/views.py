from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

from accounts.forms import UserSignUpForm
# Create your views here.
class UserSignUpView(CreateView):
	form_class = UserSignUpForm
	success_url = reverse_lazy('login')
	template_name = 'accounts/signup.html'

##########################################################
@login_required(login_url='/accounts/login/')
def change_password(request):

	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user) #importent
			"""
			Call update_session_auth_hash() after saving the form.
			Otherwise the user’s auth session will be invalidated 
			and she/he will have to log in again.
			"""
			messages.success(request, 'Your password is successfully updated! Login again to continue.')
			logout(request)
			return redirect('/accounts/login/')
		else:
			messages.error(request, 'Please correct the error below.')
			return render(request, 'accounts/change_password.html', {'form':form})
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'accounts/change_password.html', {'form':form})