"""Here are payments views."""
from django.http import JsonResponse
from django.views.generic import CreateView, ListView
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet

from payments.models import Patient, Payment
from payments.forms import PatientsFormSet, PaymentsFormSet
from payments.helpers import dehydrate_json_data


class ExtendedJsonEncoder(DjangoJSONEncoder):
    """Extend default django json serializer."""

    def default(self, o):
        """Handle object json representation."""
        if isinstance(o, Patient) or isinstance(o, Payment):
            return o.to_dict()
        elif isinstance(o, QuerySet):
            return [x.to_dict() for x in o]
        else:
            return super().default(o)


class InputJsonMixin:
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


class OutputJsonMixin:
    """Mixin which add support of JSON response with pagination."""

    paginate_by = settings.PAYMENTAGG_ITEMS_PER_PAGE

    def get_queryset(self):
        """Csutomize query set."""
        return super().get_queryset().order_by('id')

    def render_to_response(self, context, **response_kwargs):
        """Override original render_to_response method."""
        pagination = context['paginator']
        page = context['page_obj']
        data = {
            'items': page.object_list,
            'pages': pagination.num_pages,
            'page_num': page.number,
            'next_page': page.next_page_number() if page.has_next() else None,
            'prev_page': page.previous_page_number() if page.has_previous() else None
        }
        return JsonResponse(data, encoder=ExtendedJsonEncoder,
                            safe=False)


class FormsetMixin:
    """Mixin which brings formset handling.

    The idea is to process every form as separate and save the result into
    self.results list.
    """

    results = []

    def form_invalid(self, form):
        """Handle invalid data."""
        self.results.append({'status': 'fail',
                             'data': form.cleaned_data,
                             'errors': form.errors})

    def form_valid(self, form):
        """Handle valid data."""
        # INFO: handle database errors (unique constrains, everithing else)
        try:
            form.save()
        except Exception as er:
            self.results.append({'status': 'fail',
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


class FilterPatientsByPaymentAmount:
    """Filter patients by payments amount."""

    def get_queryset(self):
        """Csutomize query set."""
        queryset = super().get_queryset()
        payments_min_amount = self.request.GET.get('payments_min')
        payments_max_amount = self.request.GET.get('payments_max')

        if payments_min_amount:
            queryset = queryset.filter(
                payments__amount__gt=payments_min_amount)

        if payments_max_amount:
            queryset = queryset.filter(
                payments__amount__lt=payments_max_amount)

        return queryset.distinct()


class FilterPaymentsByPatientExternalID:
    """Filter payments by patient external id."""

    def get_queryset(self):
        """Csutomize query set."""
        queryset = super().get_queryset()
        patient_external_id = self.request.GET.get('external_id')

        if patient_external_id:
            queryset = queryset.filter(
                patient__external_id=patient_external_id)

        return queryset


class PatientsCreate(FilterPatientsByPaymentAmount,
                     InputJsonMixin, OutputJsonMixin,
                     FormsetMixin, CreateView, ListView):
    """Create new patients."""

    form_class = PatientsFormSet
    model = Patient


class PaymentsCreate(FilterPaymentsByPatientExternalID,
                     InputJsonMixin, OutputJsonMixin,
                     FormsetMixin, CreateView, ListView):
    """Create new payments."""

    form_class = PaymentsFormSet
    model = Payment
