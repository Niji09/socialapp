from django import forms
from groups.models import Group

class GroupForm(forms.ModelForm):

	class Meta():
		model=Group
		fields=['name', 'description']

		widgets = {
			'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}