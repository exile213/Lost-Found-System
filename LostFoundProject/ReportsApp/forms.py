from django import forms
from django.utils import timezone
from datetime import date, timedelta
from .models import ItemReport, Category, Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class LostItemReportForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title is required.')
        if len(title) > 100:
            raise forms.ValidationError('Title cannot exceed 100 characters.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError('Description is required.')
        if len(description) < 10:
            raise forms.ValidationError('Description must be at least 10 characters.')
        return description

    def clean_date_lost_or_found(self):
        date_lost = self.cleaned_data.get('date_lost_or_found')
        if date_lost:
            today = date.today()
            if date_lost > today:
                raise forms.ValidationError('Lost date cannot be in the future. Please select a valid date.')
            
            # Prevent dates too far in the past (more than 1 year ago)
            one_year_ago = today - timedelta(days=365)
            if date_lost < one_year_ago:
                raise forms.ValidationError('Lost date cannot be more than 1 year ago. Please select a more recent date.')
        
        return date_lost

    class Meta:
        model = ItemReport
        fields = ['title', 'description', 'category', 'location', 'date_lost_or_found', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'maxlength': 100,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., Black Laptop, Blue Backpack',
            }),
            'description': forms.Textarea(attrs={
                'minlength': 10,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Provide detailed description of your lost item...',
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'location': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'date_lost_or_found': forms.DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat(),
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Select date when item was lost',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700',
            }),
        }
        labels = {
            'title': 'Item Name',
            'description': 'Description',
            'category': 'Category',
            'location': 'Last Known Location',
            'date_lost_or_found': 'Date Lost',
            'image': 'Item Image (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
            ),
            'description',
            Row(
                Column('location', css_class='col-md-6 mb-3'),
                Column('date_lost_or_found', css_class='col-md-6 mb-3'),
            ),
            'image',
            Submit('submit', 'Report Lost Item', css_class='inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500')
        )

class FoundItemReportForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title is required.')
        if len(title) > 100:
            raise forms.ValidationError('Title cannot exceed 100 characters.')
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if not description:
            raise forms.ValidationError('Description is required.')
        if len(description) < 10:
            raise forms.ValidationError('Description must be at least 10 characters.')
        return description

    def clean_date_lost_or_found(self):
        date_found = self.cleaned_data.get('date_lost_or_found')
        if date_found:
            today = date.today()
            if date_found > today:
                raise forms.ValidationError('Found date cannot be in the future. Please select a valid date.')
            
            # Allow found items to be reported up to 30 days after finding them
            thirty_days_ago = today - timedelta(days=30)
            if date_found < thirty_days_ago:
                raise forms.ValidationError('Found date cannot be more than 30 days ago. Please report found items promptly.')
        
        return date_found

    class Meta:
        model = ItemReport
        fields = ['title', 'description', 'category', 'location', 'date_lost_or_found', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'maxlength': 100,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., Black Laptop, Blue Backpack',
            }),
            'description': forms.Textarea(attrs={
                'minlength': 10,
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Provide detailed description of the found item...',
                'rows': 4,
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'location': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            }),
            'date_lost_or_found': forms.DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat(),
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Select date when item was found',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-700',
            }),
        }
        labels = {
            'title': 'Item Name',
            'description': 'Description',
            'category': 'Category',
            'location': 'Found Location',
            'date_lost_or_found': 'Date Found',
            'image': 'Item Image (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-6 mb-3'),
                Column('category', css_class='col-md-6 mb-3'),
            ),
            'description',
            Row(
                Column('location', css_class='col-md-6 mb-3'),
                Column('date_lost_or_found', css_class='col-md-6 mb-3'),
            ),
            'image',
            Submit('submit', 'Report Found Item', css_class='inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500')
        )
