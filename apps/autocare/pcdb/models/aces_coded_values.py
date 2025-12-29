from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ACESCodedValues(AutocareAPIMetadata, models.Model):
    element = models.CharField(db_column='Element', max_length=255, null=True, blank=True)
    attribute = models.CharField(db_column='Attribute', max_length=255, null=True, blank=True)
    coded_value = models.CharField(db_column='CodedValue', max_length=255, null=True, blank=True)
    code_description = models.CharField(db_column='CodeDescription', max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."ACESCodedValues"'
        verbose_name = 'ACESCodedValues'
        verbose_name_plural = 'ACESCodedValuess'
        indexes = []

