from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class BodyType(AutocareAPIMetadata, models.Model):
    body_type_id = models.IntegerField(db_column='BodyTypeID', primary_key=True)
    body_type_name = models.CharField(db_column='BodyTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."BodyType"'
        verbose_name = 'BodyType'
        verbose_name_plural = 'BodyTypes'
        indexes = [
            models.Index(fields=['body_type_id']),
        ]

