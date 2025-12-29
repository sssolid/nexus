from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class CylinderHeadType(AutocareAPIMetadata, models.Model):
    cylinder_head_type_id = models.IntegerField(db_column='CylinderHeadTypeID', primary_key=True)
    cylinder_head_type_name = models.CharField(db_column='CylinderHeadTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."CylinderHeadType"'
        verbose_name = 'CylinderHeadType'
        verbose_name_plural = 'CylinderHeadTypes'
        indexes = [
            models.Index(fields=['cylinder_head_type_id']),
        ]

