from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Attachment(AutocareAPIMetadata, models.Model):
    attachment_id = models.IntegerField(db_column='AttachmentID', primary_key=True)
    attachment_type_id = models.IntegerField(db_column='AttachmentTypeID')
    attachment_file_name = models.CharField(db_column='AttachmentFileName', max_length=50)
    attachment_url = models.CharField(db_column='AttachmentURL', max_length=100)
    attachment_description = models.CharField(db_column='AttachmentDescription', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Attachment"'
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
        indexes = [
            models.Index(fields=['attachment_id']),
        ]

