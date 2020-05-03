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
    flight_type = forms.CharField(label='Flight Type', initial='round', required=False)

    fly_from = forms.CharField(label='From', initial='kalamata')  # TODO search using city name instead of code
    fly_to = forms.CharField(label='To', initial='bogota')
    date_from = forms.CharField(label='Date From', initial='05/06/2020')
    date_to = forms.CharField(label='Date To', initial='30/09/2020')
    return_from = forms.CharField(label='Return From', initial='05/06/2020', required=False)
    return_to = forms.CharField(label='Return To',
                                # initial=datetime.date.today,
                                initial='30/09/2020', required=False
                                )
    nights_in_dst_from = forms.IntegerField(label='Nights in destination from', initial=5, required=False)
    nights_in_dst_to = forms.IntegerField(label='Nights in destination to', initial=15, required=False)
    max_fly_duration = forms.IntegerField(label='Max of flight duration (in hours)', initial=25, required=False)
    selected_cabins = forms.CharField(label='Cabin', initial='M', required=False)
                                      # help_text="M (economy), W (economy premium), C (business), F (first class)")
    # partner_market = 'es'
    # locale = 'us'
    # curr = 'EUR'
    price_from = forms.IntegerField(label='Price from', initial=0, required=False)
    price_to = forms.IntegerField(label='Price to', initial=1200, required=False)
    max_stopovers = forms.IntegerField(label='Max stopovers', initial=3, required=False)
    # select_airlines =
    # select_airlines_exclude = False
    sort = forms.CharField(label='Sort by', initial='price', required=False)
    # asc = 1
    num_results = forms.IntegerField(label='Return the first x results', initial=5, required=True)

    def clean(self):
        data = self.cleaned_data
        return data
