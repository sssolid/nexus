from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Version(AutocareAPIMetadata, models.Model):
    padb_version = models.CharField(db_column='PAdbVersion', max_length=10, null=True, blank=True)
    padb_publication = models.DateField(db_column='PAdbPublication', null=True, blank=True)
    pcdb_publication = models.DateField(db_column='PCdbPublication', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."Version"'
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
        indexes = []

