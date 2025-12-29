from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class ChangeTableNames(AutocareAPIMetadata, models.Model):
    table_name_id = models.IntegerField(db_column='TableNameID', primary_key=True)
    table_name = models.CharField(db_column='TableName', max_length=255)
    table_description = models.CharField(db_column='TableDescription', max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."ChangeTableNames"'
        verbose_name = 'ChangeTableNames'
        verbose_name_plural = 'ChangeTableNamess'
        indexes = [
            models.Index(fields=['table_name_id']),
        ]

