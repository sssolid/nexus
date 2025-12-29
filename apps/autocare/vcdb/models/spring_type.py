from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SpringType(AutocareAPIMetadata, models.Model):
    spring_type_id = models.IntegerField(db_column='SpringTypeID', primary_key=True)
    spring_type_name = models.CharField(db_column='SpringTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."spring_type"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Spring Type'
        verbose_name_plural = 'Spring Types'
        indexes = [
            models.Index(fields=['spring_type_id'])
        ]

