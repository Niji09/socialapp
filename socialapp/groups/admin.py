from django.contrib import admin
from groups import models
# Register your models here.
class GroupMemberInline(admin.TabularInline):
	models=models.GroupMember

	"""
	visit : https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#inlinemodeladmin-objects
	
	The admin interface has the ability to edit
	models on the same page as a parent model.
	These are called inlines. 
	"""

admin.site.register(models.Group)