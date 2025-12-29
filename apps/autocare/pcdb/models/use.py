from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class Use(AutocareAPIMetadata, models.Model):
    use_id = models.IntegerField(db_column='UseID', primary_key=True)
    use_description = models.CharField(db_column='UseDescription', max_length=500)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."Use"'
        verbose_name = 'Use'
        verbose_name_plural = 'Uses'
        indexes = [
            models.Index(fields=['use_id']),
        ]

