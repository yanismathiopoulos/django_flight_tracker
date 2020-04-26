import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django import forms


class AddPositiveNumbersForm(forms.Form):
    """Form for a user to add two positive numbers."""
    first_number = forms.FloatField(
        label='First number',
        # max_value=99999999,
        help_text="Enter the first positive number")
    second_number = forms.FloatField(
        label='Second number',
        # max_value=99999999,
        help_text="Enter the second positive number")

    def clean(self):
        data = self.cleaned_data

        # Check if number is negative or zero.
        if (data['first_number'] <= 0) | (data['second_number'] <= 0):
            raise ValidationError(_('I want you to add only positive numbers'))

        # Remember to always return the cleaned data.
        return data


class RoundTripForm(forms.Form):
    """Form for a user to give inputs for a round trip."""
    apikey = forms.CharField(label='API Key', initial='hsgRmFhjJRKIzN6o0MEovJXr9VJFxQQh')

    fly_from = forms.CharField(label='From', initial='ATH')
    fly_to = forms.CharField(label='To', initial='MEX')
    date_from = forms.CharField(label='Date From', initial='01/10/2020')
    date_to = forms.CharField(label='Date To', initial='15/12/2020')
    return_from = forms.CharField(label='Return From', initial='01/10/2020')
    return_to = forms.CharField(label='Return To', initial='15/12/2020'
                                # initial=datetime.date.today
                                )
    nights_in_dst_from = forms.IntegerField(label='Nights in destination from', initial=5)
    nights_in_dst_to = forms.IntegerField(label='Nights in destination to', initial=15)
    max_fly_duration = forms.IntegerField(label='Max of flight duration (in hours)', initial=25)
    selected_cabins = forms.CharField(label='Cabin', initial='M',
                                      help_text="M (economy), W (economy premium), C (business), F (first class)")
    # 'partner_market': 'es',
    # 'locale': 'us',
    # 'curr': 'EUR',
    price_from = forms.IntegerField(label='Price from', initial=0)
    price_to = forms.IntegerField(label='Price to', initial=1200)
    max_stopovers = forms.IntegerField(label='Max stopovers', initial=3)
    sort = forms.CharField(label='Sort by', initial='price')

    def clean(self):
        data = self.cleaned_data
        return data
