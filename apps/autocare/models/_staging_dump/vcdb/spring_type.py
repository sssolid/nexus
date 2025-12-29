from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SpringType(AutocareAPIMetadata, models.Model):
    spring_type_id = models.IntegerField(db_column='SpringTypeID', primary_key=True)
    spring_type_name = models.CharField(db_column='SpringTypeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."SpringType"'
        verbose_name = 'SpringType'
        verbose_name_plural = 'SpringTypes'
        indexes = [
            models.Index(fields=['spring_type_id']),
        ]

