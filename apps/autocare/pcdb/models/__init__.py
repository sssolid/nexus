"""
PCdb (Product Component Database) models.

This module defines the Django models that correspond to the PCdb database schema.
These models represent product parts terminology, categories, positions, and part
attributes according to Auto Care Association standards.
"""
import uuid
from django.db import models


class Parts(models.Model):
    """Model for parts terminology."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_terminology_id = models.IntegerField(unique=True, db_index=True)
    part_terminology_name = models.CharField(max_length=500, db_index=True)
    parts_description = models.ForeignKey(
        'PartsDescription',
        on_delete=models.SET_NULL,
        db_column='parts_description_id',
        related_name='parts',
        null=True
    )
    rev_date = models.DateField(null=True)

    # Many-to-many relationships
    aliases = models.ManyToManyField(
        'Alias',
        through='PartsToAlias',
        related_name='parts'
    )
    uses = models.ManyToManyField(
        'Use',
        through='PartsToUse',
        related_name='parts'
    )

    class Meta:
        db_table = 'autocare_pcdb.parts'
        managed = False
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return f"{self.part_terminology_name} ({self.part_terminology_id})"


class PartsDescription(models.Model):
    """Model for parts descriptions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parts_description_id = models.IntegerField(unique=True, db_index=True)
    parts_description = models.CharField(max_length=500)

    class Meta:
        db_table = 'autocare_pcdb.parts_description'
        managed = False
        verbose_name = 'Parts Description'
        verbose_name_plural = 'Parts Descriptions'

    def __str__(self):
        return f"PartsDescription {self.parts_description_id}: {self.parts_description[:30]}..."


class Category(models.Model):
    """Model for parts categories."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.IntegerField(unique=True, db_index=True)
    category_name = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'autocare_pcdb.category'
        managed = False
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.category_name} ({self.category_id})"


class SubCategory(models.Model):
    """Model for parts subcategories."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subcategory_id = models.IntegerField(unique=True, db_index=True)
    subcategory_name = models.CharField(max_length=100, db_index=True)

    class Meta:
        db_table = 'autocare_pcdb.subcategory'
        managed = False
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return f"{self.subcategory_name} ({self.subcategory_id})"


class Position(models.Model):
    """Model for parts positions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_id = models.IntegerField(unique=True, db_index=True)
    position = models.CharField(max_length=500, db_index=True)

    class Meta:
        db_table = 'autocare_pcdb.position'
        managed = False
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return f"{self.position} ({self.position_id})"


class PartCategory(models.Model):
    """Model for parts to category mapping."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_category_id = models.IntegerField(unique=True, db_index=True)
    part = models.ForeignKey(
        Parts,
        on_delete=models.CASCADE,
        db_column='part_terminology_id',
        related_name='categories'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        db_column='subcategory_id',
        related_name='part_categories'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        db_column='category_id',
        related_name='part_categories'
    )

    class Meta:
        db_table = 'autocare_pcdb.part_category'
        managed = False
        verbose_name = 'Part Category'
        verbose_name_plural = 'Part Categories'

    def __str__(self):
        return f"PartCategory {self.part_category_id}: {self.part.part_terminology_id}"


class PartPosition(models.Model):
    """Model for parts to position mapping."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_position_id = models.IntegerField(unique=True, db_index=True)
    part = models.ForeignKey(
        Parts,
        on_delete=models.CASCADE,
        db_column='part_terminology_id',
        related_name='positions'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        db_column='position_id',
        related_name='part_positions'
    )
    rev_date = models.DateField(null=True)

    class Meta:
        db_table = 'autocare_pcdb.part_position'
        managed = False
        verbose_name = 'Part Position'
        verbose_name_plural = 'Part Positions'

    def __str__(self):
        return f"PartPosition {self.part_position_id}: {self.part.part_terminology_id}"


class PartsSupersession(models.Model):
    """Model for parts supersession."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parts_supersession_id = models.IntegerField(unique=True, db_index=True)
    old_part_terminology_id = models.IntegerField()
    old_part_terminology_name = models.CharField(max_length=256)
    new_part_terminology_id = models.IntegerField()
    new_part_terminology_name = models.CharField(max_length=256)
    rev_date = models.DateField(null=True)
    note = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'autocare_pcdb.parts_supersession'
        managed = False
        verbose_name = 'Parts Supersession'
        verbose_name_plural = 'Parts Supersessions'

    def __str__(self):
        return f"PartsSupersession {self.parts_supersession_id}: {self.old_part_terminology_id} -> {self.new_part_terminology_id}"


class CodeMaster(models.Model):
    """Model for code master which links parts, categories, subcategories, and positions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_master_id = models.IntegerField(unique=True, db_index=True)
    part = models.ForeignKey(
        Parts,
        on_delete=models.CASCADE,
        db_column='part_terminology_id'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        db_column='category_id',
        related_name='code_masters'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        db_column='subcategory_id',
        related_name='code_masters'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        db_column='position_id',
        related_name='code_masters'
    )
    rev_date = models.DateField()

    class Meta:
        db_table = 'autocare_pcdb.code_master'
        managed = False
        verbose_name = 'Code Master'
        verbose_name_plural = 'Code Masters'

    def __str__(self):
        return f"CodeMaster {self.code_master_id}: {self.part.part_terminology_id}"


class Alias(models.Model):
    """Model for part aliases."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias_id = models.IntegerField(unique=True, db_index=True)
    alias_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'autocare_pcdb.alias'
        managed = False
        verbose_name = 'Alias'
        verbose_name_plural = 'Aliases'

    def __str__(self):
        return f"{self.alias_name} ({self.alias_id})"


class PartsToAlias(models.Model):
    """Association model for parts to aliases."""

    part = models.ForeignKey(
        Parts,
        on_delete=models.CASCADE,
        db_column='part_terminology_id'
    )
    alias = models.ForeignKey(
        Alias,
        on_delete=models.CASCADE,
        db_column='alias_id'
    )

    class Meta:
        db_table = 'autocare_pcdb.parts_to_alias'
        managed = False
        unique_together = ['part', 'alias']
        verbose_name = 'Parts to Alias'
        verbose_name_plural = 'Parts to Aliases'

    def __str__(self):
        return f"Part {self.part.part_terminology_id} -> Alias {self.alias.alias_id}"


class Use(models.Model):
    """Model for part uses."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    use_id = models.IntegerField(unique=True, db_index=True)
    use_description = models.CharField(max_length=100)

    class Meta:
        db_table = 'autocare_pcdb.use'
        managed = False
        verbose_name = 'Use'
        verbose_name_plural = 'Uses'

    def __str__(self):
        return f"{self.use_description} ({self.use_id})"


class PartsToUse(models.Model):
    """Association model for parts to uses."""

    part = models.ForeignKey(
        Parts,
        on_delete=models.CASCADE,
        db_column='part_terminology_id'
    )
    use = models.ForeignKey(
        Use,
        on_delete=models.CASCADE,
        db_column='use_id'
    )

    class Meta:
        db_table = 'autocare_pcdb.parts_to_use'
        managed = False
        unique_together = ['part', 'use']
        verbose_name = 'Parts to Use'
        verbose_name_plural = 'Parts to Uses'

    def __str__(self):
        return f"Part {self.part.part_terminology_id} -> Use {self.use.use_id}"


class PCdbVersion(models.Model):
    """Model for PCdb version tracking."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_date = models.DateTimeField(db_index=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        db_table = 'autocare_pcdb.pcdb_version'
        managed = False
        verbose_name = 'PCdb Version'
        verbose_name_plural = 'PCdb Versions'

    def __str__(self):
        return f"PCdbVersion {self.version_date.strftime('%Y-%m-%d')}"
