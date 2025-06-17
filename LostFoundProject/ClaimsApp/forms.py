from django import forms
from .models import ClaimRequest

class ClaimRequestForm(forms.ModelForm):
    class Meta:
        model = ClaimRequest
        fields = ['reason', 'additional_proof']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 4,
                'placeholder': 'Explain why you believe this item belongs to you. Provide specific details about the item to help us verify your claim.'
            }),
            'additional_proof': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
            }),
        }
        labels = {
            'reason': 'Why do you believe this item belongs to you?',
            'additional_proof': 'Proof of Ownership (Optional)',
        } 