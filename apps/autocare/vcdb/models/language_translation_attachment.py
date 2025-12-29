from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class LanguageTranslationAttachment(AutocareAPIMetadata, models.Model):
    language_translation_attachment_id = models.IntegerField(db_column='LanguageTranslationAttachmentID', primary_key=True)
    language_translation_id = models.IntegerField(db_column='LanguageTranslationID')
    attachment_id = models.IntegerField(db_column='AttachmentID')

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."language_translation_attachment"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Language Translation Attachment'
        verbose_name_plural = 'Language Translation Attachments'
        indexes = [
            models.Index(fields=['language_translation_attachment_id'])
        ]

