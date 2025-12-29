from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class VcdbVersion(AutocareAPIMetadata, models.Model):
    version_date = models.DateField(db_column='VersionDate')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."version"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'

