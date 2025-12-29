from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PIESExpiGroup(AutocareAPIMetadata, models.Model):
    pies_expi_group_id = models.IntegerField(db_column='PIESExpiGroupId', primary_key=True)
    expi_group_code = models.CharField(db_column='ExpiGroupCode', max_length=500)
    expi_group_description = models.CharField(db_column='ExpiGroupDescription', max_length=500)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PIESExpiGroup"'
        verbose_name = 'PIESExpiGroup'
        verbose_name_plural = 'PIESExpiGroups'
        indexes = [
            models.Index(fields=['pies_expi_group_id']),
        ]

