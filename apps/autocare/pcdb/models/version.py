from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Version(AutocareAPIMetadata, models.Model):
    version_date = models.DateTimeField(db_column='VersionDate', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Version"'
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        indexes = []

