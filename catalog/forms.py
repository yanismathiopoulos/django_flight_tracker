from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms


class AddPositiveNumbersForm(forms.Form):
    """Form for a user to add two positive numbers."""
    first_number = forms.FloatField(
            help_text="Enter the first number")
    second_number = forms.FloatField(
            help_text="Enter the second number")

    def clean_numbers(self):
        data = self.cleaned_data['positive_number']

        # Check if number is negative or zero.
        if data <= 0:
            raise ValidationError(_('Invalid number - is negative or zero'))

        # Remember to always return the cleaned data.
        return data
