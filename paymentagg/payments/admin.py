"""Options of /admin/payments."""

from django.contrib import admin
from payments.models import Patient, Payment


class BaseAdmin(admin.ModelAdmin):
    """Base admin class."""

    extra_list_display = ('created', 'updated')
    readonly_fields = ('created', 'updated')

    def get_list_display(self, request):
        """Customize get list display."""
        return self.list_display + self.extra_list_display


class PatientAdmin(BaseAdmin):
    """Handle /admin/payments/patients."""

    list_display = ('id', 'external_id', 'first_name', 'middle_name',
                    'last_name')
    list_filter = ('created', 'date_of_birth')


class PaymentAdmin(BaseAdmin):
    """Handle /admin/payments/payments."""

    list_display = ('id', 'external_id', 'amount', 'patient')
    list_filter = ('created', )

    def patient(self, obj):
        """Get the patient full name."""
        return str(obj.patient)


admin.site.register(Patient, PatientAdmin)
admin.site.register(Payment, PaymentAdmin)
