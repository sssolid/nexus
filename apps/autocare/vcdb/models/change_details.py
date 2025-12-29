from django.db import models
from apps.autocare.models.mixins import AutocareAPIMetadata


class ChangeDetails(AutocareAPIMetadata, models.Model):
    change_detail_id = models.IntegerField(db_column='ChangeDetailID', primary_key=True)
    changes = models.ForeignKey('autocare_vcdb.Changes', db_column='ChangeID', db_index=True, on_delete=models.DO_NOTHING)
    change_attribute_states = models.ForeignKey('autocare_vcdb.ChangeAttributeStates', db_column='ChangeAttributeStateID', db_index=True, on_delete=models.DO_NOTHING)
    change_table_names = models.ForeignKey('autocare_vcdb.ChangeTableNames', db_column='TableNameID', db_index=True, on_delete=models.DO_NOTHING)
    primary_key_column_name = models.CharField(db_column='PrimaryKeyColumnName', max_length=255, blank=True, null=True)
    primary_key_before = models.IntegerField(db_column='PrimaryKeyBefore', blank=True, null=True)
    primary_key_after = models.IntegerField(db_column='PrimaryKeyAfter', blank=True, null=True)
    column_name = models.CharField(db_column='ColumnName', max_length=255, blank=True, null=True)
    column_value_before = models.CharField(db_column='ColumnValueBefore', max_length=1000, blank=True, null=True)
    column_value_after = models.CharField(db_column='ColumnValueAfter', max_length=1000, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.pk})"

    class Meta:
        managed = True
        db_table = '"autocare_vcdb"."change_details"'
        app_label = 'autocare_vcdb'
        verbose_name = 'Change Details'
        verbose_name_plural = 'Change Details'
        indexes = [
            models.Index(fields=['change_detail_id'])
        ]

