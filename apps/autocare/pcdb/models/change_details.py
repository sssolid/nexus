from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ChangeDetails(AutocareAPIMetadata, models.Model):
    change_detail_id = models.IntegerField(db_column='ChangeDetailID', primary_key=True)
    change = models.ForeignKey('autocare_pcdb.Changes', db_column='ChangeID', db_index=True, on_delete=models.DO_NOTHING)
    change_attribute_state = models.ForeignKey('autocare_pcdb.ChangeAttributeStates', db_column='ChangeAttributeStateID', db_index=True, on_delete=models.DO_NOTHING)
    table_name = models.ForeignKey('autocare_pcdb.ChangeTableNames', db_column='TableNameID', db_index=True, on_delete=models.DO_NOTHING)
    primary_key_column_name = models.CharField(db_column='PrimaryKeyColumnName', max_length=255, null=True, blank=True)
    primary_key_before = models.IntegerField(db_column='PrimaryKeyBefore', null=True, blank=True)
    primary_key_after = models.IntegerField(db_column='PrimaryKeyAfter', null=True, blank=True)
    column_name = models.CharField(db_column='ColumnName', max_length=255, null=True, blank=True)
    column_value_before = models.CharField(db_column='ColumnValueBefore', max_length=1000, null=True, blank=True)
    column_value_after = models.CharField(db_column='ColumnValueAfter', max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        app_label = 'autocare_pcdb'
        managed = True
        db_table = '"autocare_pcdb"."ChangeDetails"'
        verbose_name = 'ChangeDetails'
        verbose_name_plural = 'ChangeDetailss'
        indexes = [
            models.Index(fields=['change_detail_id']),
        ]

