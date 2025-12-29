from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Positions(AutocareAPIMetadata, models.Model):
    position_id = models.IntegerField(db_column='PositionID', primary_key=True)
    position = models.CharField(db_column='Position', max_length=500)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Positions"'
        verbose_name = 'Positions'
        verbose_name_plural = 'Positionss'
        indexes = [
            models.Index(fields=['position_id']),
        ]

