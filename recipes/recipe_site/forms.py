from django import forms
from tinymce.widgets import TinyMCE
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ('owner', 'name', 'description', 'cooking_order', 'cover' )
        widgets = {
            'description': TinyMCE(),
            'cooking_order': TinyMCE(),
            'owner': forms.HiddenInput(),
                    }    