from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class LanguageTranslation(AutocareAPIMetadata, models.Model):
    language_translation_id = models.IntegerField(db_column='LanguageTranslationID', primary_key=True)
    english_phrase_id = models.IntegerField(db_column='EnglishPhraseID')
    language_id = models.IntegerField(db_column='LanguageID')
    translation = models.CharField(db_column='Translation', max_length=150)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."LanguageTranslation"'
        verbose_name = 'LanguageTranslation'
        verbose_name_plural = 'LanguageTranslations'
        indexes = [
            models.Index(fields=['language_translation_id']),
        ]

