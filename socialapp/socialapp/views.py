from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePage( LoginRequiredMixin, TemplateView):
	login_url = '/accounts/login/'
	template_name = 'posts/post_list.html'