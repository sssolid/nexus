from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class PartCategory(AutocareAPIMetadata, models.Model):
    part_category_id = models.IntegerField(
        db_column="PartCategoryID",
        primary_key=True,
    )

    part_terminology_id = models.IntegerField(
        db_column="PartTerminologyID",
        db_index=True,
    )

    subcategory_id = models.IntegerField(
        db_column="SubCategoryID",
        db_index=True,
    )

    category_id = models.IntegerField(
        db_column="CategoryID",
        db_index=True,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = "autocare_pcdb"
        managed = True
        db_table = '"autocare_pcdb"."PartCategory"'
        verbose_name = "PartCategory"
        verbose_name_plural = "PartCategories"
        indexes = [
            models.Index(fields=["part_terminology_id"]),
            models.Index(fields=["subcategory_id"]),
            models.Index(fields=["category_id"]),
        ]
