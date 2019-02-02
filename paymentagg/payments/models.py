"""Here is the payment aggregator models."""
from django.db import models


class Base(models.Model):
    """Base model class, all other should be inherited from it."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Model options."""

        abstract = True


class Patient(Base):
    """Patient profile."""

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    external_id = models.CharField(max_length=250, unique=True)

    def __str__(self):
        """Represent object."""
        return '{0} {1} <extID:{2}>'.format(
            self.first_name, self.last_name, self.external_id)

    class Meta:
        """Model options."""

        db_table = 'patients'


class Payment(Base):
    """Payment profile."""

    amount = models.DecimalField(max_digits=9, decimal_places=3)
    patient = models.ForeignKey(Patient, related_name='payments',
                                on_delete=models.CASCADE)
    external_id = models.CharField(max_length=250, unique=True)

    class Meta:
        """Model options."""

        db_table = 'payments'
