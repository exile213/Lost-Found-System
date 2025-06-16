from django import forms
from .models import ItemReport, Category, Location
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class LostItemReportForm(forms.ModelForm):
    class Meta:
        model = ItemReport
        fields = ['title', 'description', 'category', 'location', 'date_lost_or_found', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., Black Laptop, Blue Backpack',
            }),
            'description': forms.Textarea(attrs={
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
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
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
    class Meta:
        model = ItemReport
        fields = ['title', 'description', 'category', 'location', 'date_lost_or_found', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., Black Laptop, Blue Backpack',
            }),
            'description': forms.Textarea(attrs={
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
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
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
