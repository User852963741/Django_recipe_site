from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Ingredient(models.Model):
    name = models.CharField(_('name'), max_length=200, help_text=_('enter ingredient name (in plural form if possible)'))

    UNITS_OF_MEASURE = (
        ('kg', _('kilos')),
        ('g', _('grams')),
        ('u', _('units')),
        ('ts', _('teaspoons')),
        ('tbls', _('table spoons')),
    )

    measurement_unit = models.CharField(_('measured in'), max_length=1, choices=UNITS_OF_MEASURE, default='g',)

    def __str__(self):
        return f'{self.name} measured in {self.measurement_unit}'

class Recipe(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='recipes',
        verbose_name=_('owner'),
    )
    