import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django import forms


class RoundTripForm(forms.Form):
    """Form for a user to give inputs for a round trip."""
    # TODO validate inputs (add error handling for wrong inputs)
    # TODO drop down menus etc
    apikey = forms.CharField(label='API Key', initial='hsgRmFhjJRKIzN6o0MEovJXr9VJFxQQh')
    flight_type = forms.CharField(label='Flight Type', initial='round')

    fly_from = forms.CharField(label='From', initial='ATH')  # TODO search using city name instead of code
    fly_to = forms.CharField(label='To', initial='MEX')
    date_from = forms.CharField(label='Date From', initial='01/10/2020')
    date_to = forms.CharField(label='Date To', initial='15/12/2020')
    return_from = forms.CharField(label='Return From', initial='01/10/2020')
    return_to = forms.CharField(label='Return To',
                                # initial=datetime.date.today,
                                initial='15/12/2020'
                                )
    nights_in_dst_from = forms.IntegerField(label='Nights in destination from', initial=5)
    nights_in_dst_to = forms.IntegerField(label='Nights in destination to', initial=15)
    max_fly_duration = forms.IntegerField(label='Max of flight duration (in hours)', initial=25)
    selected_cabins = forms.CharField(label='Cabin', initial='M',
                                      help_text="M (economy), W (economy premium), C (business), F (first class)")
    # partner_market = 'es'
    # locale = 'us'
    # curr = 'EUR'
    price_from = forms.IntegerField(label='Price from', initial=0)
    price_to = forms.IntegerField(label='Price to', initial=1200)
    max_stopovers = forms.IntegerField(label='Max stopovers', initial=3)
    # select_airlines =
    # select_airlines_exclude = False
    sort = forms.CharField(label='Sort by', initial='price')
    # asc = 1

    def clean(self):
        data = self.cleaned_data
        return data
