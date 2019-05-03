from django.db import models
from django.urls import reverse
from django.conf import settings
from groups.models import Group
from django.contrib.auth import get_user_model

# to get the current loggied in user
User = get_user_model()

# Create your models here.
class Post(models.Model):
	user= models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now=True)
	message = models.TextField()
	group = models.ForeignKey(Group, related_name='posts_group', null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.message

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

	"""
	def get_absolute_url(self):
		return reverse('posts:single', kwargs={
				'username':self.user.username,
				'pk':self.pk,
		})
	"""
	def get_absolute_url(self):
		return reverse('posts:all')


	class Meta:
		ordering = ['-created_at']
		unique_together = ['user', 'message', 'group']
