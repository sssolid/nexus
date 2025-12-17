from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class CylinderHeadType(AutocareAPIMetadata, models.Model):
    cylinder_head_type_id = models.IntegerField(db_column='CylinderHeadTypeID', primary_key=True)
    cylinder_head_type_name = models.CharField(db_column='CylinderHeadTypeName', max_length=30)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."cylinder_head_type"'
        verbose_name = 'Cylinder Head Type'
        verbose_name_plural = 'Cylinder Head Types'
        indexes = [
            models.Index(fields=['cylinder_head_type_id'])
        ]

