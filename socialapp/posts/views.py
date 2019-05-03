from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from groups.models import Group


from posts import models
from posts import forms

User = get_user_model()
# Create your views here.
class PostList(LoginRequiredMixin, ListView):
	login_url = '/accounts/login/'
	model = models.Post
	select_related = ('user', 'group')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['group_list'] = Group.objects.all()
		return context

class UserPosts(ListView):
	model = models.Post
	template_name = 'posts/user_post_list.html'

	def get_queryset(self):
		try:
			self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
		except User.DoesNotExist:
			raise Http404
		else:
			return self.post_user.posts.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_user'] = self.post_user
		return context

class PostDetail(SelectRelatedMixin, DetailView):
	login_url = '/accounts/login/'
	model = models.Post
	select_related = ('user', 'group')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
	login_url = '/accounts/login/'
	form_class= forms.PostForm
	model = models.Post

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, SelectRelatedMixin, UpdateView):
	login_url = '/accounts/login/'
	form_class= forms.PostForm
	model = models.Post
	select_related =  ('user', 'group')

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
	login_url = '/accounts/login/'
	model = models.Post
	select_related = ('user', 'group')
	success_url = reverse_lazy('posts:all')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user_id=self.request.user.id)

	def delete(self, *args, **kwargs):
		messages.success(self.request, 'Post Deleted')
		return super().delete(*args, **kwargs)
