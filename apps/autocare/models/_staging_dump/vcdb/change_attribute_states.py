from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ChangeAttributeStates(AutocareAPIMetadata, models.Model):
    change_attribute_state_id = models.IntegerField(db_column='ChangeAttributeStateID', primary_key=True)
    change_attribute_state = models.CharField(db_column='ChangeAttributeState', max_length=255)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."ChangeAttributeStates"'
        verbose_name = 'ChangeAttributeStates'
        verbose_name_plural = 'ChangeAttributeStatess'
        indexes = [
            models.Index(fields=['change_attribute_state_id']),
        ]

