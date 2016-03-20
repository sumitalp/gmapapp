__author__ = 'ahsan'

from django.forms.models import ModelForm
from .models import Unit


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ('lat', 'lng', 'address')
