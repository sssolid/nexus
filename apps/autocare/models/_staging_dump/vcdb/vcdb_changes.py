from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class VCdbChanges(AutocareAPIMetadata, models.Model):
    version_date = models.DateTimeField(db_column='VersionDate')
    table_name = models.CharField(db_column='TableName', max_length=30)
    id = models.IntegerField(db_column='ID')
    action = models.CharField(db_column='Action', max_length=1)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."VCdbChanges"'
        verbose_name = 'VCdbChanges'
        verbose_name_plural = 'VCdbChangess'
        indexes = []

