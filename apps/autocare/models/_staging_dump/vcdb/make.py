from django.db import models
from apps.autocare.core.mixins import AutocareAPIMetadata


class Make(AutocareAPIMetadata, models.Model):
    make_id = models.IntegerField(db_column='MakeID', primary_key=True)
    make_name = models.CharField(db_column='MakeName', max_length=50)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_vcdb'
        managed = True
        db_table = '"autocare_vcdb"."Make"'
        verbose_name = 'Make'
        verbose_name_plural = 'Makes'
        indexes = [
            models.Index(fields=['make_id']),
        ]

