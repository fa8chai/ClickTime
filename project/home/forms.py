from django.contrib.auth.forms import forms
from .models import Post, Image
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django.conf import settings

   
      
class PostForm(forms.ModelForm):
      class Meta:
            model = Post
            fields=['text']
      
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'placeholder':('Write something...'),'class':('form-control post-text text-break'), 'rows':2})