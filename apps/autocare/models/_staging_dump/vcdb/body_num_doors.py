from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class BodyNumDoors(AutocareAPIMetadata, models.Model):
    body_num_doors_id = models.IntegerField(db_column='BodyNumDoorsID', primary_key=True)
    body_num_doors = models.CharField(db_column='BodyNumDoors', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BodyNumDoors"'
        verbose_name = 'BodyNumDoors'
        verbose_name_plural = 'BodyNumDoorss'
        indexes = [
            models.Index(fields=['body_num_doors_id']),
        ]

