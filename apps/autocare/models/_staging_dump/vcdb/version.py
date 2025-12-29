from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Version(AutocareAPIMetadata, models.Model):
    version_date = models.DateField(db_column='VersionDate')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Version"'
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        indexes = []

