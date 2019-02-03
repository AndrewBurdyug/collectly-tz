"""Load data from json file."""
import argparse

from django.core.management.base import BaseCommand, CommandError

from payments.helpers import dehydrate_json_data
from payments.forms import PatientsFormSet, PaymentsFormSet


class Command(BaseCommand):
    """Handle command."""

    help = 'Load data from json file.'

    def add_arguments(self, parser):
        """Add arguments to command."""
        parser.add_argument(
            '--input-file', type=argparse.FileType('r'), required=True)
        parser.add_argument(
            '--model-name', type=str, choices=['patient', 'payment'],
            required=True,
            help='choose the model (available: patient, payment)')

    def form_valid(self, form):
        """Handle valid form."""
        try:
            form.save()
        except Exception as er:
            self.stderr.write(
                self.style.ERROR(
                    'Failed load: {0}, erorrs: {1}'.format(
                        form.cleaned_data, str(er))))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully load: {0}'.format(
                        form.cleaned_data)))

    def form_invalid(self, form):
        """Handle invalid form."""
        self.stderr.write(
            self.style.ERROR(
                'Failed load: {0}, errors: {1}'.format(
                    form.cleaned_data, dict(form.errors))))

    def handle(self, *args, **options):
        """Doing action."""
        model_name = options['model_name']
        input_file = options['input_file']
        data = dehydrate_json_data(None, input_file)

        if model_name == 'patient':
            formset = PatientsFormSet(data)
        elif model_name == 'payment':
            formset = PaymentsFormSet(data)
        else:
            raise CommandError('Unknown model name')

        for form in formset:
            if form.is_valid():
                self.form_valid(form)
            else:
                self.form_invalid(form)
