from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PublicationStage(AutocareAPIMetadata, models.Model):
    publication_stage_id = models.IntegerField(db_column='PublicationStageID', primary_key=True)
    publication_stage_name = models.CharField(db_column='PublicationStageName', max_length=100)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."PublicationStage"'
        verbose_name = 'PublicationStage'
        verbose_name_plural = 'PublicationStages'
        indexes = [
            models.Index(fields=['publication_stage_id']),
        ]

