from django import forms
from tinymce.widgets import TinyMCE
from . import models


class RecipeForm(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ('owner', 'name', 'description', 'cooking_order', 'cover' )
        widgets = {
            'description': TinyMCE(),
            'cooking_order': TinyMCE(),
            'owner': forms.HiddenInput(),
                    }    


class UserRecipeForm(forms.ModelForm):
    class Meta:
        model = models.UserRecipe
        fields = ('user', 'recipe', 'rating', 'favourite', 'note', )
        widgets = {
            'note': TinyMCE(),
            'user': forms.HiddenInput(),
                    }    