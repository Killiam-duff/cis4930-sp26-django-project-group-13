from django import forms
from .models import Record

#samples for now
class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["name", "category", "value"]

    def clean_value(self):
        value = self.cleaned_data["value"]
        if value < 0:
            raise forms.ValidationError("Value must be positive.")
        return value
