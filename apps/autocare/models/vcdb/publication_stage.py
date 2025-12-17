from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PublicationStage(AutocareAPIMetadata, models.Model):
    publication_stage_id = models.IntegerField(db_column='PublicationStageID', primary_key=True)
    publication_stage_name = models.CharField(db_column='PublicationStageName', max_length=100)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."publication_stage"'
        verbose_name = 'Publication Stage'
        verbose_name_plural = 'Publication Stages'
        indexes = [
            models.Index(fields=['publication_stage_id'])
        ]

