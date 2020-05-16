import datetime as dt
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django import forms
from .widgets import BootstrapDateTimePickerInput, XDSoftDateTimePickerInput
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Row, Column
from django.urls import reverse

datepicker_widget = DatePickerInput(
    options={'format': 'DD/MM/YYYY',  # moment date-time format
             'showClose': True,
             'showClear': True,
             'showTodayButton': True})


class FlightSearchInputForm(forms.Form):
    """Form for a user to give inputs for a round trip."""

    flight_type = forms.ChoiceField(label='Flight Type',
                                    initial='round',
                                    choices=(('round', 'Return'),
                                             ('oneway', 'One way')))
    fly_from = forms.CharField(label='Fly from',
                               initial='Barcelona',
                               max_length=20)
    fly_to = forms.CharField(label='Fly to',
                             # initial='Madrid',
                             widget=forms.TextInput(attrs={'placeholder': 'try a destination...'}),
                             max_length=20)
    date_from = forms.DateTimeField(label='Departure date from',
                                    initial=dt.datetime.today().strftime('%d/%m/%Y'),
                                    # initial='15/06/2020',
                                    input_formats=['%d/%m/%Y'],
                                    widget=datepicker_widget)
    date_to = forms.DateTimeField(label='Departure date to',
                                  initial=(dt.datetime.today() + dt.timedelta(days=1)).strftime('%d/%m/%Y'),
                                  input_formats=['%d/%m/%Y'],
                                  widget=datepicker_widget)
    return_from = forms.DateTimeField(label='Return date from',
                                      initial=(dt.datetime.today() + dt.timedelta(days=7)).strftime('%d/%m/%Y'),
                                      input_formats=['%d/%m/%Y'],
                                      widget=datepicker_widget,
                                      required=False)
    return_to = forms.DateTimeField(label='Return date to',
                                    initial=(dt.datetime.today() + dt.timedelta(days=8)).strftime('%d/%m/%Y'),
                                    input_formats=['%d/%m/%Y'],
                                    widget=datepicker_widget,
                                    required=False)
    nights_in_dst_from = forms.IntegerField(label='Nights in destination from',
                                            # initial=5,
                                            min_value=0, max_value=360,
                                            required=False)
    nights_in_dst_to = forms.IntegerField(label='Nights in destination to',
                                          # initial=15,
                                          min_value=0, max_value=360,
                                          required=False)
    max_fly_duration = forms.IntegerField(label='Max of flight duration',
                                          # initial=25,
                                          min_value=0, max_value=100,
                                          required=False)
    selected_cabins = forms.ChoiceField(label='Cabin', initial='M',
                                        choices=(('M', 'Economy'),
                                                 ('W', 'Economy Premium'),
                                                 ('C', 'Business'),
                                                 ('F', 'First Class')))
    # partner_market = 'es'
    # locale = 'us'
    # curr = 'EUR'
    price_from = forms.IntegerField(label='Price from',
                                    # initial=0,
                                    min_value=0, max_value=10000,
                                    required=False)
    price_to = forms.IntegerField(label='Price to',
                                  # initial=1200,
                                  min_value=0, max_value=10000,
                                  required=False)
    max_stopovers = forms.IntegerField(label='Max stopovers',
                                       # initial=3,
                                       min_value=0, max_value=10,
                                       required=False)
    # select_airlines =
    # select_airlines_exclude = False
    sort = forms.ChoiceField(label='Sort by', initial='quality',
                             choices=(('quality', 'Best'),
                                      ('price', 'Price'),
                                      ('duration', 'Duration'),
                                      ('date', 'Date')))
    # asc = 1
    num_results = forms.IntegerField(label='Options to show', initial=10, min_value=1, max_value=150, required=True)

    def __init__(self, *args, **kwargs):
        super(FlightSearchInputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'flight_search_input_form'
        # self.helper.form_id = 'flight_search_input_form'
        # self.helper.form_method = 'post'
        # self.helper.form_action = reverse('index')
        # self.helper.add_input(Submit('submit', 'Submit'))

        flight_type = self.fields.get('flight_type')
        if flight_type == 'oneway':
            self.fields['nights_in_dst_from'].widget.attrs['disabled'] = 'true'

        self.helper.layout = Layout(
            Row(Column('flight_type', css_class='form-group col-md-6 mb-0'),
                # Column('apikey', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Row(Column('fly_from', css_class='form-group col-md-6 mb-0'),
                Column('fly_to', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            # Row(Div('Departure')),  # TODO Add text 'departure'
            Row(Column('date_from', css_class='form-group col-md-6 mb-0'),
                Column('date_to', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Row(Column('return_from', css_class='form-group col-md-6 mb-0'),
                Column('return_to', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Row(Column('nights_in_dst_from', css_class='form-group col-md-6 mb-0'),
                Column('nights_in_dst_to', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Row(Column('price_from', css_class='form-group col-md-6 mb-0'),
                Column('price_to', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Row(Column('max_fly_duration', css_class='form-group col-md-4 mb-0'),
                Column('selected_cabins', css_class='form-group col-md-4 mb-0'),
                Column('max_stopovers', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
                ),
            Row(Column('sort', css_class='form-group col-md-6 mb-0'),
                Column('num_results', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
                ),
            Submit('submit', 'Submit')
        )

    def clean(self):
        # data = self.cleaned_data
        data = super().clean()

        if data['flight_type'] == 'oneway':
            # user inputs return dates
            if data['return_from'] is not None or data['return_to'] is not None:
                raise ValidationError('No return dates required in one-way flights. Please clear selection.')

            # user inputs nights_in_dst
            if data['nights_in_dst_from'] is not None or data['nights_in_dst_to'] is not None:
                raise ValidationError('No nights in destination required in one-way flights. Please clear selection.')

        if data['flight_type'] == 'round':
            # user didn't specify neither return dates nor nights_in_dst
            if (data['return_from'] is None or data['return_to'] is None) \
                    and (
                    data['nights_in_dst_from'] is None or data['nights_in_dst_to'] is None):
                raise ValidationError('Please specify return dates or nights in destination period.')

            # user chose both nights_in_dst
            elif data['nights_in_dst_from'] is not None and data['nights_in_dst_to'] is not None:
                # user also chose one from return dates
                if (data['return_from'] is None and data['return_to'] is not None) or \
                        (data['return_from'] is not None and data['return_to'] is None):
                    raise ValidationError('Please specify both return dates.')

            # user chose both return dates
            elif data['return_from'] is not None and data['return_to'] is not None:
                # user also chose one from nights_in_dst
                if (data['nights_in_dst_from'] is None and data['nights_in_dst_to'] is not None) or \
                        (data['nights_in_dst_from'] is not None and data['nights_in_dst_to'] is None):
                    raise ValidationError('Please specify full nights in destination period.')

                # user chose return dates earlier than departure dates
                if (data['return_from'] < data['date_from']) or \
                        (data['return_to'] < data['date_to']):
                    raise ValidationError('Return date cannot be earlier than departure date.')

                # user chose return date to earlier than return date from
                if data['return_to'] < data['return_from']:
                    raise ValidationError('Return date to cannot be earlier than return date from.')

        # user chose departure date to earlier than departure date from
        if data['date_to'] < data['date_from']:
            raise ValidationError('Departure date to cannot be earlier than departure date from.')

        return data
