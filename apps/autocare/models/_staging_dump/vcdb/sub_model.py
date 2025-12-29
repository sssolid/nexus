from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class SubModel(AutocareAPIMetadata, models.Model):
    submodel_id = models.IntegerField(db_column='SubmodelID', primary_key=True)
    sub_model_name = models.CharField(db_column='SubModelName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."SubModel"'
        verbose_name = 'SubModel'
        verbose_name_plural = 'SubModels'
        indexes = [
            models.Index(fields=['submodel_id']),
        ]

