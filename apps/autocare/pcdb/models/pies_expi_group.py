from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PIESExpiGroup(AutocareAPIMetadata, models.Model):
    id = models.BigAutoField(primary_key=True)

    pies_expi_group_id = models.IntegerField(
        db_column="PIESExpiGroupId",
        null=True,
        blank=True,
        db_index=True,
    )

    expi_group_code = models.CharField(
        db_column="ExpiGroupCode",
        max_length=500,
    )

    expi_group_description = models.CharField(
        db_column="ExpiGroupDescription",
        max_length=500,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PIESExpiGroup"'
        unique_together = [
            ("pies_expi_group_id", "expi_group_code"),
        ]
        indexes = [
            models.Index(fields=["pies_expi_group_id"]),
        ]
        verbose_name = "PIES Expi Group"
        verbose_name_plural = "PIES Expi Groups"
