from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESExpiCode(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_expi_code_id = models.IntegerField(
        db_column="PIESExpiCodeId",
        null=True,
        blank=True,
        db_index=True,
    )

    expi_code = models.CharField(
        db_column="ExpiCode",
        max_length=100,
    )

    expi_code_description = models.CharField(
        db_column="ExpiCodeDescription",
        max_length=500,
    )

    pies_expi_group = models.ForeignKey(
        "autocare_pcdb.PIESExpiGroup",
        db_column="PIESExpiGroupId",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESExpiCode"'
        unique_together = [
            ("pies_expi_code_id", "expi_code"),
        ]
        indexes = [
            models.Index(fields=["pies_expi_code_id"]),
        ]
        verbose_name = "PIES Expi Code"
        verbose_name_plural = "PIES Expi Codes"
