"""
PAdb (Part Attribute Database) models.

This module defines the Django models that correspond to the PAdb database schema.
These models represent part attribute definitions, metadata, and valid values according
to Auto Care Association standards.
"""
import uuid
from django.db import models


class PartAttribute(models.Model):
    """Model for part attribute definitions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pa_id = models.IntegerField(unique=True, db_index=True)
    pa_name = models.CharField(max_length=80, null=True)
    pa_descr = models.CharField(max_length=512, null=True)

    class Meta:
        db_table = 'autocare_padb.part_attribute'
        managed = False
        verbose_name = 'Part Attribute'
        verbose_name_plural = 'Part Attributes'

    def __str__(self):
        return f"{self.pa_name} ({self.pa_id})"


class MetaData(models.Model):
    """Model for attribute metadata definitions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_id = models.IntegerField(unique=True, db_index=True)
    meta_name = models.CharField(max_length=80, null=True)
    meta_descr = models.CharField(max_length=512, null=True)
    meta_format = models.CharField(max_length=10, null=True)
    data_type = models.CharField(max_length=50, null=True)
    min_length = models.IntegerField(null=True)
    max_length = models.IntegerField(null=True)

    class Meta:
        db_table = 'autocare_padb.metadata'
        managed = False
        verbose_name = 'Meta Data'
        verbose_name_plural = 'Meta Data'

    def __str__(self):
        return f"{self.meta_name} ({self.meta_id})"


class MeasurementGroup(models.Model):
    """Model for measurement groupings."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    measurement_group_id = models.IntegerField(unique=True, db_index=True)
    measurement_group_name = models.CharField(max_length=80, null=True)

    class Meta:
        db_table = 'autocare_padb.measurement_group'
        managed = False
        verbose_name = 'Measurement Group'
        verbose_name_plural = 'Measurement Groups'

    def __str__(self):
        return f"{self.measurement_group_name} ({self.measurement_group_id})"


class MetaUOMCode(models.Model):
    """Model for units of measure codes."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_uom_id = models.IntegerField(unique=True, db_index=True)
    uom_code = models.CharField(max_length=10, null=True)
    uom_description = models.CharField(max_length=512, null=True)
    uom_label = models.CharField(max_length=10, null=True)
    measurement_group = models.ForeignKey(
        MeasurementGroup,
        on_delete=models.PROTECT,
        db_column='measurement_group_id',
        related_name='uom_codes'
    )

    class Meta:
        db_table = 'autocare_padb.meta_uom_code'
        managed = False
        verbose_name = 'Meta UOM Code'
        verbose_name_plural = 'Meta UOM Codes'

    def __str__(self):
        return f"{self.uom_code} ({self.meta_uom_id})"


class PartAttributeAssignment(models.Model):
    """Model for assignments between parts, attributes, and metadata."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    papt_id = models.IntegerField(unique=True, db_index=True)
    part_terminology_id = models.IntegerField()  # Foreign key to pcdb.parts
    attribute = models.ForeignKey(
        PartAttribute,
        on_delete=models.CASCADE,
        db_column='pa_id',
        related_name='assignments'
    )
    metadata_info = models.ForeignKey(
        MetaData,
        on_delete=models.PROTECT,
        db_column='meta_id',
        related_name='assignments'
    )

    class Meta:
        db_table = 'autocare_padb.part_attribute_assignment'
        managed = False
        verbose_name = 'Part Attribute Assignment'
        verbose_name_plural = 'Part Attribute Assignments'

    def __str__(self):
        return f"PartAttributeAssignment {self.papt_id}: {self.part_terminology_id}"


class MetaUomCodeAssignment(models.Model):
    """Model for assignments between attributes and UOM codes."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meta_uom_code_assignment_id = models.IntegerField(unique=True, db_index=True)
    attribute_assignment = models.ForeignKey(
        PartAttributeAssignment,
        on_delete=models.CASCADE,
        db_column='papt_id',
        related_name='uom_assignments'
    )
    meta_uom = models.ForeignKey(
        MetaUOMCode,
        on_delete=models.PROTECT,
        db_column='meta_uom_id',
        related_name='assignments'
    )

    class Meta:
        db_table = 'autocare_padb.meta_uom_code_assignment'
        managed = False
        verbose_name = 'Meta UOM Code Assignment'
        verbose_name_plural = 'Meta UOM Code Assignments'

    def __str__(self):
        return f"MetaUomCodeAssignment {self.meta_uom_code_assignment_id}"


class ValidValue(models.Model):
    """Model for valid values for attributes."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    valid_value_id = models.IntegerField(unique=True, db_index=True)
    valid_value = models.CharField(max_length=500)

    class Meta:
        db_table = 'autocare_padb.valid_value'
        managed = False
        verbose_name = 'Valid Value'
        verbose_name_plural = 'Valid Values'

    def __str__(self):
        return f"ValidValue {self.valid_value_id}: {self.valid_value[:30]}..."


class ValidValueAssignment(models.Model):
    """Model for assignments between attributes and valid values."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    valid_value_assignment_id = models.IntegerField(unique=True, db_index=True)
    attribute_assignment = models.ForeignKey(
        PartAttributeAssignment,
        on_delete=models.CASCADE,
        db_column='papt_id',
        related_name='valid_value_assignments'
    )
    valid_value = models.ForeignKey(
        ValidValue,
        on_delete=models.PROTECT,
        db_column='valid_value_id',
        related_name='assignments'
    )

    class Meta:
        db_table = 'autocare_padb.valid_value_assignment'
        managed = False
        verbose_name = 'Valid Value Assignment'
        verbose_name_plural = 'Valid Value Assignments'

    def __str__(self):
        return f"ValidValueAssignment {self.valid_value_assignment_id}"


class Style(models.Model):
    """Model for style definitions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    style_id = models.IntegerField(unique=True, db_index=True, null=True)
    style_name = models.CharField(max_length=225, null=True)

    class Meta:
        db_table = 'autocare_padb.style'
        managed = False
        verbose_name = 'Style'
        verbose_name_plural = 'Styles'

    def __str__(self):
        return f"{self.style_name} ({self.style_id})"


class PartAttributeStyle(models.Model):
    """Model for part attribute styling."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    style_id = models.IntegerField(null=True)  # References Style but not enforced FK
    attribute_assignment = models.ForeignKey(
        PartAttributeAssignment,
        on_delete=models.CASCADE,
        db_column='papt_id',
        related_name='style',
        null=True
    )

    class Meta:
        db_table = 'autocare_padb.part_attribute_style'
        managed = False
        verbose_name = 'Part Attribute Style'
        verbose_name_plural = 'Part Attribute Styles'

    def __str__(self):
        return f"PartAttributeStyle {self.id}: {self.attribute_assignment.papt_id if self.attribute_assignment else 'N/A'}"


class PartTypeStyle(models.Model):
    """Model for part type styling."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    style = models.ForeignKey(
        Style,
        on_delete=models.SET_NULL,
        db_column='style_id',
        related_name='part_type_styles',
        null=True
    )
    part_terminology_id = models.IntegerField(null=True)  # Foreign key to pcdb.parts

    class Meta:
        db_table = 'autocare_padb.part_type_style'
        managed = False
        verbose_name = 'Part Type Style'
        verbose_name_plural = 'Part Type Styles'

    def __str__(self):
        return f"PartTypeStyle {self.id}: {self.part_terminology_id}"


class PAdbVersion(models.Model):
    """Model for PAdb version tracking."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_date = models.DateTimeField(db_index=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        db_table = 'autocare_padb.padb_version'
        managed = False
        verbose_name = 'PAdb Version'
        verbose_name_plural = 'PAdb Versions'

    def __str__(self):
        return f"PAdbVersion {self.version_date.strftime('%Y-%m-%d')}"
