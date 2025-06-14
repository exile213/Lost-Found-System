from django import forms
from .models import ClaimRequest

class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['reason', 'additional_proof']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md',
                'placeholder': 'Explain why you are claiming this item...'
            }),
            'additional_proof': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700',
            }),
        }
        labels = {
            'reason': 'Reason for Claim',
            'additional_proof': 'Additional Proof (optional)',
        } 