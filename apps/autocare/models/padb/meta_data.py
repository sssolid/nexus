from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class MetaData(AutocareAPIMetadata, models.Model):
    meta_id = models.IntegerField(db_column='MetaID', primary_key=True)
    meta_name = models.CharField(db_column='MetaName', max_length=80, null=True, blank=True)
    meta_descr = models.CharField(db_column='MetaDescr', max_length=512, null=True, blank=True)
    meta_format = models.CharField(db_column='MetaFormat', max_length=10, null=True, blank=True)
    data_type = models.CharField(db_column='DataType', max_length=50, null=True, blank=True)
    min_length = models.IntegerField(db_column='MinLength', null=True, blank=True)
    max_length = models.IntegerField(db_column='MaxLength', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_padb'
        managed = True
        db_table = '"autocare_padb"."MetaData"'
        verbose_name = 'MetaData'
        verbose_name_plural = 'MetaDatas'
        indexes = [
            models.Index(fields=['meta_id']),
        ]

