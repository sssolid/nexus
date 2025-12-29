from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Attachment(AutocareAPIMetadata, models.Model):
    attachment_id = models.IntegerField(db_column='AttachmentID', primary_key=True)
    attachment_type = models.ForeignKey(
        "autocare_vcdb.PIESCode",
        to_field="pies_code_id",
        db_column="AttachmentTypeID",
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
    )
    attachment_file_name = models.CharField(db_column='AttachmentFileName', max_length=50)
    attachment_url = models.CharField(db_column='AttachmentURL', max_length=100)
    attachment_description = models.CharField(db_column='AttachmentDescription', max_length=50)

    def __str__(self) -> str:
        return f"{self.attachment_type} - {self.attachment_file_name}"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."attachment"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
        indexes = [
            models.Index(fields=['attachment_id']),
            models.Index(fields=['attachment_type'])
        ]

