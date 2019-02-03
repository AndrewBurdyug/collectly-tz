"""Here are forms of payments models."""
from datetime import datetime
from django.forms import (ModelForm, ModelChoiceField, formset_factory,
                          ValidationError)

from payments.models import Patient, Payment


class PatientForm(ModelForm):
    """Form for patient data validation."""

    def clean_date_of_birth(self):
        """Validate date of birth."""
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > datetime.utcnow().date():
            raise ValidationError('Date of birth cannot be in future')
        if date_of_birth.year <= 1900:
            raise ValidationError(
                'Date of birth cannot be less or equal than 1900')
        return date_of_birth

    class Meta:
        """Form options."""

        model = Patient
        fields = '__all__'


class PaymentForm(ModelForm):
    """Form for payment data validation."""

    patient = ModelChoiceField(queryset=Patient.objects.all(),
                               to_field_name='external_id')

    class Meta:
        """Form options."""

        model = Payment
        fields = '__all__'


PatientsFormSet = formset_factory(PatientForm)
PaymentsFormSet = formset_factory(PaymentForm)
