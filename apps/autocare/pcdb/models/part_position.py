from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartPosition(AutocareAPIMetadata, models.Model):
    part_position_id = models.IntegerField(
        db_column="PartPositionID",
        primary_key=True,
    )

    part_terminology_id = models.IntegerField(
        db_column="PartTerminologyID",
        db_index=True,
    )

    position_id = models.IntegerField(
        db_column="PositionID",
        db_index=True,
    )

    rev_date = models.DateField(
        db_column="RevDate",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PartPosition"'
        verbose_name = "PartPosition"
        verbose_name_plural = "PartPositions"
        indexes = [
            models.Index(fields=["part_terminology_id"]),
            models.Index(fields=["position_id"]),
        ]
