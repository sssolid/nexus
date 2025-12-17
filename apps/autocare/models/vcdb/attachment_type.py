from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class AttachmentType(AutocareAPIMetadata, models.Model):
    attachment_type_id = models.IntegerField(db_column='AttachmentTypeID', primary_key=True)
    attachment_type_name = models.CharField(db_column='AttachmentTypeName', max_length=20)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."attachment_type"'
        verbose_name = 'Attachment Type'
        verbose_name_plural = 'Attachment Types'
        indexes = [
            models.Index(fields=['attachment_type_id'])
        ]

