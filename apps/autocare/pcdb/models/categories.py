from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Categories(AutocareAPIMetadata, models.Model):
    category_id = models.IntegerField(db_column='CategoryID', primary_key=True)
    category_name = models.CharField(db_column='CategoryName', max_length=500)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Categories"'
        verbose_name = 'Categories'
        verbose_name_plural = 'Categoriess'
        indexes = [
            models.Index(fields=['category_id']),
        ]

