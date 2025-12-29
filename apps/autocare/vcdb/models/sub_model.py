from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class SubModel(AutocareAPIMetadata, models.Model):
    submodel_id = models.IntegerField(db_column='SubmodelID', primary_key=True)
    sub_model_name = models.CharField(db_column='SubModelName', max_length=50)

    def __str__(self) -> str:
        return f"{self.sub_model_name} ({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."sub_model"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Sub Model'
        verbose_name_plural = 'Sub Models'
        indexes = [
            models.Index(fields=['submodel_id'])
        ]

