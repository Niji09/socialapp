from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, RedirectView
from groups.models import Group
from django.contrib import messages
from groups.forms import GroupForm
from groups.models import Group,GroupMember
# Create your views here.

class CreateGroup(LoginRequiredMixin, CreateView):
	form_class= GroupForm
	model = Group

	def form_valid(self, form):
		form.instance.group_admin = self.request.user
		return super().form_valid(form)

class SingleGroup(DetailView):
	model = Group

class ListGroup(ListView):
	model = Group

class JoinGroup(LoginRequiredMixin, RedirectView):

	def get_redirect_url(self, *args, **kwargs):
		return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):
		group=get_object_or_404(Group, slug=self.kwargs.get('slug'))

		try:
			GroupMember.objects.create(user=self.request.user, group=group)
		except Exception as e:
			messages.warning(self.request, 'Warning : Already a member!')
		else:
			messages.success(self.request, 'You are a member now!')

		return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, RedirectView):
	
	def get_redirect_url(self, *args, **kwargs):
		return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

	def get(self, request, *args, **kwargs):

		try:
			membership = GroupMember.objects.filter(
				user=self.request.user,
				group__slug = self.kwargs.get('slug')
			).get()
		except models.GroupMember.DoesNotExist:
			messages.warning(self.request, 'Sorry you are not member of this group!')
		else:
			membership.delete()
			messages.success(self.request, 'You have left the group!')

		return super().get(request, *args, **kwargs)