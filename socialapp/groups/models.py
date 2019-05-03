from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

from django import template
register = template.Library()

# Create your models here.
class Group(models.Model):
	group_admin = models.ForeignKey(User, related_name='group_admin_user', on_delete=models.CASCADE, default=1)
	name = models.CharField(max_length=256, unique=True)
	slug = models.SlugField(allow_unicode=True, unique=True)
	description = models.TextField(blank=True, default='')
	members = models.ManyToManyField(User, through='GroupMember')
	#sometimes you may need to associate data with the relationship between two models.
	#The intermediate model is associated with the ManyToManyField using the "through" 
	#...argument to point to the model that will act as an intermediary.

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('groups:single', kwargs={'slug':self.slug})

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['group_list'] = Group.objects.all()
		return context

	class Meta:
		ordering = ['name']
		#The default ordering for the object, for use when obtaining lists of objects


class GroupMember(models.Model):
	group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

	class Meta:
		unique_together = ['group', 'user']