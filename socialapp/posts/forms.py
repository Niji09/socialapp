from django import forms
from posts.models import Post

class PostForm(forms.ModelForm):

	class Meta():
		model=Post
		fields=['message', 'group']

		widgets = {
			'message': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}