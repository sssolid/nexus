"""
Qdb (Qualifier Database) models.

This module defines the Django models that correspond to the Qdb database schema.
These models represent qualifiers and their translations according to Auto Care
Association standards.
"""
import uuid
from django.db import models


class QualifierType(models.Model):
    """Model for qualifier types."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualifier_type_id = models.IntegerField(unique=True, db_index=True)
    qualifier_type = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'autocare_qdb.qualifier_type'
        managed = False
        verbose_name = 'Qualifier Type'
        verbose_name_plural = 'Qualifier Types'

    def __str__(self):
        return f"{self.qualifier_type} ({self.qualifier_type_id})"


class Qualifier(models.Model):
    """Model for qualifiers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualifier_id = models.IntegerField(unique=True, db_index=True)
    qualifier_text = models.CharField(max_length=500, null=True)
    example_text = models.CharField(max_length=500, null=True)
    qualifier_type = models.ForeignKey(
        QualifierType,
        on_delete=models.PROTECT,
        db_column='qualifier_type_id',
        related_name='qualifiers'
    )
    new_qualifier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        db_column='new_qualifier_id',
        related_name='supersedes',
        null=True
    )
    when_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'autocare_qdb.qualifier'
        managed = False
        verbose_name = 'Qualifier'
        verbose_name_plural = 'Qualifiers'
        constraints = [
            models.UniqueConstraint(fields=['qualifier_id'], name='uq_qualifier_id')
        ]

    def __str__(self):
        text = self.qualifier_text or ""
        return f"Qualifier {self.qualifier_id}: {text[:30]}..."


class QLanguage(models.Model):
    """Model for languages."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language_id = models.IntegerField(unique=True, db_index=True)
    language_name = models.CharField(max_length=50, null=True)
    dialect_name = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'autocare_qdb.language'
        managed = False
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return f"{self.language_name} ({self.language_id})"


class QualifierTranslation(models.Model):
    """Model for qualifier translations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualifier_translation_id = models.IntegerField(unique=True, db_index=True)
    qualifier = models.ForeignKey(
        Qualifier,
        on_delete=models.CASCADE,
        db_column='qualifier_id',
        related_name='translations'
    )
    language = models.ForeignKey(
        QLanguage,
        on_delete=models.PROTECT,
        db_column='language_id',
        related_name='translations'
    )
    translation_text = models.CharField(max_length=500)

    class Meta:
        db_table = 'autocare_qdb.qualifier_translation'
        managed = False
        verbose_name = 'Qualifier Translation'
        verbose_name_plural = 'Qualifier Translations'

    def __str__(self):
        return f"QualifierTranslation {self.qualifier_translation_id}: {self.translation_text[:30]}..."


class GroupNumber(models.Model):
    """Model for qualifier group numbers."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_number_id = models.IntegerField(unique=True, db_index=True)
    group_description = models.CharField(max_length=100)

    class Meta:
        db_table = 'autocare_qdb.group_number'
        managed = False
        verbose_name = 'Group Number'
        verbose_name_plural = 'Group Numbers'

    def __str__(self):
        return f"GroupNumber {self.group_number_id}: {self.group_description}"


class QualifierGroup(models.Model):
    """Model for qualifier groups."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualifier_group_id = models.IntegerField(unique=True, db_index=True)
    group_number = models.ForeignKey(
        GroupNumber,
        on_delete=models.CASCADE,
        db_column='group_number_id',
        related_name='qualifier_groups'
    )
    qualifier = models.ForeignKey(
        Qualifier,
        on_delete=models.CASCADE,
        db_column='qualifier_id',
        related_name='groups'
    )

    class Meta:
        db_table = 'autocare_qdb.qualifier_group'
        managed = False
        verbose_name = 'Qualifier Group'
        verbose_name_plural = 'Qualifier Groups'

    def __str__(self):
        return f"QualifierGroup {self.qualifier_group_id}: {self.group_number_id}/{self.qualifier_id}"


class QdbVersion(models.Model):
    """Model for Qdb version tracking."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_date = models.DateTimeField(db_index=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        db_table = 'autocare_qdb.qdb_version'
        managed = False
        verbose_name = 'Qdb Version'
        verbose_name_plural = 'Qdb Versions'

    def __str__(self):
        return f"QdbVersion {self.version_date.strftime('%Y-%m-%d')}"
