from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BodyNumDoors(AutocareAPIMetadata, models.Model):
    body_num_doors_id = models.IntegerField(db_column='BodyNumDoorsID', primary_key=True)
    body_num_doors = models.CharField(db_column='BodyNumDoors', max_length=3)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."body_num_doors"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Body Num Doors'
        verbose_name_plural = 'Body Num Doors'
        indexes = [
            models.Index(fields=['body_num_doors_id'])
        ]

