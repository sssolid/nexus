from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class PIESSegment(AutocareAPIMetadata, models.Model):
    pies_segment_id = models.IntegerField(db_column='PIESSegmentId', primary_key=True)
    segment_abb = models.CharField(db_column='SegmentAbb', max_length=100)
    segment_name = models.CharField(db_column='SegmentName', max_length=100)
    segment_description = models.CharField(db_column='SegmentDescription', max_length=250)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."PIESSegment"'
        verbose_name = 'PIESSegment'
        verbose_name_plural = 'PIESSegments'
        indexes = [
            models.Index(fields=['pies_segment_id']),
        ]

