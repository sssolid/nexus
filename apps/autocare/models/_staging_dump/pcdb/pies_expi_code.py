from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESExpiCode(AutocareAPIMetadata, models.Model):
    pies_expi_code_id = models.IntegerField(db_column='PIESExpiCodeId', primary_key=True)
    expi_code = models.CharField(db_column='ExpiCode', max_length=100)
    expi_code_description = models.CharField(db_column='ExpiCodeDescription', max_length=500)
    pies_expi_group = models.ForeignKey('autocare_pcdb.PIESExpiGroup', db_column='PIESExpiGroupId', db_index=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PIESExpiCode"'
        verbose_name = 'PIESExpiCode'
        verbose_name_plural = 'PIESExpiCodes'
        indexes = [
            models.Index(fields=['pies_expi_code_id']),
        ]

