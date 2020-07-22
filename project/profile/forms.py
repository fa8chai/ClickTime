from django.contrib.auth.forms import forms
from .models import Profile
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django.conf import settings
from users.models import CustomUser

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html =  Template("""
                              <span class="image-upload"><input id="id_picture" type="file" name="picture" onchange="document.querySelector('.image1').src = window.URL.createObjectURL(this.files[0])"></span>
                        """)
        return mark_safe(html.substitute(media=settings.MEDIA_URL,link=value))



class ProfileForm(forms.ModelForm):
      picture = ImageField(widget=PictureWidget, label='')
      class Meta:
            model = Profile
            fields=['picture','username','bio']

      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':('form-control'),})
        self.fields['bio'].widget.attrs.update({'class':('form-control'),'rows':4})
        self.fields['picture'].required = False
