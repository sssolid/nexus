from django import forms

from apps.autocare.vcdb.models.attachment import Attachment
# from apps.autocare.models.reference import PIESCode


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["attachment_type"].queryset = (
        #     PIESCode.objects.filter(
        #         reference_fields__pies_field_id=32
        #     )
        # )
