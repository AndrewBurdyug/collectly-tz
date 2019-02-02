"""Here are forms of payments models."""
from django.forms import ModelForm, ModelChoiceField
from payments.models import Patient, Payment


class PatientForm(ModelForm):
    """Form for patient data validation."""

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
