from django.db import models


class AutocareAPIMetadata(models.Model):
    """
    Fields present on Autocare API records but not necessarily in upstream DB schema.
    Stored on our model instances for convenience during materialization.
    """

    culture_id = models.CharField(
        # db_column='CultureID',
        max_length=10,
        null=True,
        blank=True,
        help_text="CultureID from Autocare API (e.g. en-US).",
    )

    effective_datetime = models.DateTimeField(
        # db_column='EffectiveDateTime',
        null=True,
        blank=True,
        help_text="EffectiveDateTime from Autocare API (ISO-8601).",
    )

    end_datetime = models.DateTimeField(
        # db_column='EndDateTime',
        null=True,
        blank=True,
        help_text="EndDateTime from Autocare API (ISO-8601).",
    )

    class Meta:
        abstract = True
