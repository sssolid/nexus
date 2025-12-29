from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Language(AutocareAPIMetadata, models.Model):
    language_id = models.IntegerField(db_column='LanguageID', primary_key=True)
    language_name = models.CharField(db_column='LanguageName', max_length=20)
    dialect_name = models.CharField(db_column='DialectName', max_length=20, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."language"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        indexes = [
            models.Index(fields=['language_id'])
        ]

