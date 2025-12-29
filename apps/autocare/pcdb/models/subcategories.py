from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Subcategories(AutocareAPIMetadata, models.Model):
    sub_category_id = models.IntegerField(db_column='SubCategoryID', primary_key=True)
    sub_category_name = models.CharField(db_column='SubCategoryName', max_length=500)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Subcategories"'
        verbose_name = 'Subcategories'
        verbose_name_plural = 'Subcategoriess'
        indexes = [
            models.Index(fields=['sub_category_id']),
        ]

