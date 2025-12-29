from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class EnglishPhrase(AutocareAPIMetadata, models.Model):
    english_phrase_id = models.IntegerField(db_column='EnglishPhraseID', primary_key=True)
    english_phrase = models.CharField(db_column='EnglishPhrase', max_length=100)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."english_phrase"'
        app_label = 'autocare_vcdb'
        verbose_name = 'English Phrase'
        verbose_name_plural = 'English Phrases'
        indexes = [
            models.Index(fields=['english_phrase_id'])
        ]

