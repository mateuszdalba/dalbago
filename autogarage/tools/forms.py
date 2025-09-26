from django import forms
from .models import Toolbox

class ToolboxReferenceForm(forms.ModelForm):
    class Meta:
        model = Toolbox
        fields = ["weight_ref"]
        widgets = {
            "weight_ref": forms.NumberInput(attrs={
                "class": "border rounded p-2 w-40",
                "step": "0.01",
            }),
        }
        labels = {
            "weight_ref": "Reference Weight (g)",
        }
