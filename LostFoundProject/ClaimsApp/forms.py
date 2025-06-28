from django import forms
from django.utils import timezone
from datetime import date, timedelta
from .models import ClaimRequest

class ClaimRequestForm(forms.ModelForm):
    def clean_reason(self):
        reason = self.cleaned_data.get('reason', '').strip()
        if not reason:
            raise forms.ValidationError('Reason is required.')
        if len(reason) < 10:
            raise forms.ValidationError('Reason must be at least 10 characters.')
        if len(reason) > 1000:
            raise forms.ValidationError('Reason cannot exceed 1000 characters.')
        return reason

    def clean_additional_proof(self):
        proof = self.cleaned_data.get('additional_proof')
        if proof:
            # Check file size (10MB limit)
            if proof.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError('File size must be under 10MB.')
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'text/plain']
            if proof.content_type not in allowed_types:
                raise forms.ValidationError('Please upload a valid file type (JPG, PNG, GIF, PDF, or TXT).')
        
        return proof

    class Meta:
        model = ClaimRequest
        fields = ['reason', 'additional_proof']
        widgets = {
            'reason': forms.Textarea(attrs={
                'minlength': 10,
                'maxlength': 1000,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 4,
                'placeholder': 'Explain why you believe this item belongs to you. Provide specific details about the item to help us verify your claim.'
            }),
            'additional_proof': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
                'accept': 'image/*,.pdf,.txt',
            }),
        }
        labels = {
            'reason': 'Why do you believe this item belongs to you?',
            'additional_proof': 'Proof of Ownership (Optional)',
        } 