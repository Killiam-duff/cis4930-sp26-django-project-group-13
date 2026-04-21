from django import forms

from .models import BattingRecord


class BattingRecordForm(forms.ModelForm):
    class Meta:
        model = BattingRecord
        exclude = ['source', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
