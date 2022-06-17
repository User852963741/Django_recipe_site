from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from tinymce.models import HTMLField

class Ingredient(models.Model):
    name = models.CharField(_('name'), max_length=200, help_text=_('enter ingredient name (in plural form if possible)'))

    UNITS_OF_MEASURE = (
        ('kg', _('kilograms')),
        ('g', _('grams')),
        ('l', _('liters')),
        ('ml', _('mililiters')),
        ('u', _('units')),
        ('ts', _('teaspoons')),
        ('tbls', _('table spoons')),
        ('c', _('cups')),
    )

    measurement_unit = models.CharField(_('measured in'), max_length=4, choices=UNITS_OF_MEASURE, default='g',)

    def __str__(self):
        return f'{str(self.name)} measured in {str(self.measurement_unit)}'
    
    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        ordering = ('name', )

class Recipe(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name=_('owner'),
    )
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), max_length=1000, help_text=_('add a short description of the recipe'))
    coooking_order = HTMLField(_('cooking order'), help_text=_('describe how the recipe should be cooked'))
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    cover = models.ImageField(_('cover'), upload_to='recipe_site/covers', null=True, blank=True)

    def __str__(self):
        return f'{str(self.name)}'

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        ordering = ('created_at', )

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'{str(self.ingredient.name)} in {str(self.recipe.name)}'

class UserRecipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    RATING_CHOICES = zip( range(1,11), range(1,11) )
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True)
    favourite = models.BooleanField(default=False)
    note = models.TextField(_('private note'), max_length=1000, help_text=_('add a private note to yourself about this recipe'))

    def __str__(self):
        return f'{str(self.user)} - {str(self.recipe.name)}'