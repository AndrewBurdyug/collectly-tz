"""Here are payments views."""
# from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.forms import formset_factory
from django.core.serializers.json import DjangoJSONEncoder

from payments.models import Patient
from payments.forms import PatientForm, PaymentForm
from payments.helpers import dehydrate_json_data


class ExtendedJsonEncoder(DjangoJSONEncoder):
    """Extend default django json serializer."""

    def default(self, o):
        """Handle object json representation."""
        if isinstance(o, Patient):
            return 'Patient object'
        else:
            return super().default(o)


class JsonMixin:
    """Mixin which add support of JSON input data processing.

    If input JSON data contain the json field names in camelCase it will
    be converted to snake case for seamless django form processing.

    Also as we expect the list of items, the resulting data will be
    converted to formset data (including management data).
    """

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            if self.request.content_type == 'application/json':
                try:
                    kwargs['data'] = dehydrate_json_data(self.request.body)
                except Exception as er:
                    raise
                    return JsonResponse({'status': 'fail', 'errors': str(er)})
            else:
                kwargs.update({
                    # TODO: process data submitted via html forms
                    'data': self.request.POST,
                    'files': self.request.FILES,
                })
        return kwargs


class FormsetMixin:
    """Mixin which brings formset handling.

    The idea is to process every form as separate and save the result into
    self.results list.
    """

    results = []

    def form_invalid(self, form):
        """Handle invalid data."""
        self.results.append({'status': 'fail invalid form',
                             'data': form.cleaned_data,
                             'errors': form.errors})

    def form_valid(self, form):
        """Handle valid data."""
        # INFO: handle database errors (unique constrains, everithing else)
        try:
            form.save()
        except Exception as er:
            self.results.append({'status': 'fail save failed',
                                 'data': form.cleaned_data,
                                 'errors': str(er)})
        else:
            self.results.append({'status': 'success',
                                 'data': form.cleaned_data})

    def post(self, request, *args, **kwargs):
        """Handle POST request."""
        self.results = []
        formset = self.get_form()
        for form in formset:
            if form.is_valid():
                self.form_valid(form)
            else:
                self.form_invalid(form)
        return JsonResponse(self.results, encoder=ExtendedJsonEncoder,
                            safe=False)


class PatientsCreate(JsonMixin, FormsetMixin, CreateView):
    """Create new patients."""

    form_class = formset_factory(PatientForm)


class PaymentsCreate(JsonMixin, FormsetMixin, CreateView):
    """Create new payments."""

    form_class = formset_factory(PaymentForm)
