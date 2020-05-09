import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django import forms
from .widgets import BootstrapDateTimePickerInput, XDSoftDateTimePickerInput
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from django.urls import reverse

datepicker_widget = DatePickerInput(
    options={'format': 'DD/MM/YYYY',  # moment date-time format
             'showClose': True,
             'showClear': True,
             'showTodayButton': True})


class RoundTripForm(forms.Form):
    """Form for a user to give inputs for a round trip."""

    # TODO validate inputs (add error handling for wrong inputs)
    # TODO drop down menus etc

    def __init__(self, *args, **kwargs):
        super(RoundTripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-personal-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('index')
        self.helper.add_input(Submit('submit', 'Submit'))

    apikey = forms.CharField(label='API Key', initial='hsgRmFhjJRKIzN6o0MEovJXr9VJFxQQh')
    # flight_type = forms.CharField(label='Flight Type', initial='round', required=False)
    flight_type = forms.ChoiceField(label='Flight Type',
                                    initial='round',
                                    choices=(("1", "round"),
                                             ("2", "oneway")))
    fly_from = forms.CharField(label='From', initial='kalamata')  # TODO search using city name instead of code
    fly_to = forms.CharField(label='To', initial='bogota')
    date_from = forms.DateTimeField(label='Date From',
                                    initial='15/06/2020',
                                    input_formats=['%d/%m/%Y'],
                                    widget=datepicker_widget)
    date_to = forms.DateTimeField(label='Date To',
                                  initial='30/09/2020',
                                  input_formats=['%d/%m/%Y'],
                                  widget=datepicker_widget)
    return_from = forms.DateTimeField(label='Return From',
                                      initial='15/06/2020',
                                      input_formats=['%d/%m/%Y'],
                                      widget=datepicker_widget,
                                      required=False)
    return_to = forms.DateTimeField(label='Return To',
                                    # initial=datetime.date.today,
                                    initial='30/09/2020',
                                    input_formats=['%d/%m/%Y'],
                                    widget=datepicker_widget,
                                    required=False)
    nights_in_dst_from = forms.IntegerField(label='Nights in destination from', initial=5, min_value=0, required=False)
    nights_in_dst_to = forms.IntegerField(label='Nights in destination to', initial=15, min_value=0, required=False)
    max_fly_duration = forms.IntegerField(label='Max of flight duration (in hours)', initial=25, min_value=0, required=False)
    selected_cabins = forms.ChoiceField(label='Cabin', initial='M',
                                        choices=(('1', 'M'),
                                                 ('2', 'W'),
                                                 ('3', 'C'),
                                                 ('4', 'F')))  # TODO separate label with input
    # help_text="M (economy), W (economy premium), C (business), F (first class)")
    # partner_market = 'es'
    # locale = 'us'
    # curr = 'EUR'
    price_from = forms.IntegerField(label='Price from', initial=0, min_value=0, required=False)
    price_to = forms.IntegerField(label='Price to', initial=1200, max_value=10000, required=False)
    max_stopovers = forms.IntegerField(label='Max stopovers', initial=3, min_value=0, required=False)
    # select_airlines =
    # select_airlines_exclude = False
    sort = forms.ChoiceField(label='Sort by', initial='price',
                             choices=(('1', 'price'),
                                      ('2', 'duration'),
                                      ('3', 'quality'),
                                      ('4', 'date')))
    # asc = 1
    num_results = forms.IntegerField(label='Return the first x results', initial=5, min_value=0, required=True)

    def clean(self):
        # data = self.cleaned_data
        data = super().clean()
        return data
