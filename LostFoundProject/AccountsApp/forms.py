from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Enhanced registration form with proper validations and constraints"""
    
    # Custom validators
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    student_id_regex = RegexValidator(
        regex=r'^[A-Za-z0-9]{6,20}$',
        message="Student/Staff ID must be 6-20 characters long and contain only letters and numbers."
    )
    
    # Form fields with enhanced validation
    username = forms.CharField(
        max_length=150,
        min_length=3,
        validators=[
            MinLengthValidator(3, "Username must be at least 3 characters long."),
            MaxLengthValidator(150, "Username cannot exceed 150 characters."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Your username (3-150 characters)',
        }),
        help_text="Required. 3-150 characters. Letters, digits and @/./+/-/_ only."
    )
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'student@chmsu.edu.ph',
        }),
        help_text="Only @chmsu.edu.ph email addresses are allowed for registration."
    )
    
    password1 = forms.CharField(
        min_length=8,
        max_length=128,
        validators=[
            MinLengthValidator(8, "Password must be at least 8 characters long."),
        ],
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 pr-10',
            'placeholder': '•••••••• (min 8 characters)',
        }),
        help_text="Password must be at least 8 characters long.",
        label="Password"
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 pr-10',
            'placeholder': '••••••••',
        }),
        help_text="Enter the same password as before, for verification.",
        label="Confirm Password"
    )
    
    first_name = forms.CharField(
        max_length=150,
        min_length=1,
        validators=[
            MinLengthValidator(1, "First name cannot be empty."),
            MaxLengthValidator(150, "First name cannot exceed 150 characters."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'First name',
        }),
        help_text="Enter your first name."
    )
    
    last_name = forms.CharField(
        max_length=150,
        min_length=1,
        validators=[
            MinLengthValidator(1, "Last name cannot be empty."),
            MaxLengthValidator(150, "Last name cannot exceed 150 characters."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Last name',
        }),
        help_text="Enter your last name."
    )
    
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': '(123) 456-7890',
        }),
        help_text="Enter your phone number in international format."
    )
    
    student_id = forms.CharField(
        max_length=20,
        min_length=6,
        validators=[student_id_regex],
        widget=forms.TextInput(attrs={
            'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'e.g. 2023123456',
        }),
        help_text="Enter your student ID (6-20 characters, letters and numbers only)."
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded',
        }),
        help_text="You must agree to the terms and conditions."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 
                 'phone_number', 'student_id', 'terms_accepted')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Check for valid characters
            if not re.match(r'^[a-zA-Z0-9@.+\-_]+$', username):
                raise ValidationError("Username can only contain letters, numbers, and @/./+/-/_ characters.")
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                raise ValidationError("This username is already taken. Please choose a different one.")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email address is already registered. Please use a different email or try logging in.")
            
            # Basic email format validation
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError("Please enter a valid email address.")
            
            # Check for chmsu.edu.ph domain
            email_domain = email.split('@')[1].lower() if '@' in email else ''
            if email_domain != 'chmsu.edu.ph':
                raise ValidationError("Only @chmsu.edu.ph email addresses are allowed for registration.")
        
        return email
    
    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            # Check password strength - only length requirement
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Automatically assign student role to new registrations
        user.role = 'student'
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """Enhanced profile editing form with proper validations"""
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    student_id_regex = RegexValidator(
        regex=r'^[A-Za-z0-9]{6,20}$',
        message="Student/Staff ID must be 6-20 characters long and contain only letters and numbers."
    )
    
    first_name = forms.CharField(
        max_length=150,
        min_length=1,
        validators=[
            MinLengthValidator(1, "First name cannot be empty."),
            MaxLengthValidator(150, "First name cannot exceed 150 characters."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        }),
    )
    
    last_name = forms.CharField(
        max_length=150,
        min_length=1,
        validators=[
            MinLengthValidator(1, "Last name cannot be empty."),
            MaxLengthValidator(150, "Last name cannot exceed 150 characters."),
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
        }),
    )
    
    phone_number = forms.CharField(
        max_length=15,
        validators=[phone_regex],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your phone number',
        }),
    )
    
    student_id = forms.CharField(
        max_length=20,
        min_length=6,
        validators=[student_id_regex],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your student/staff ID',
        }),
    )
    
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100',
            'accept': 'image/*',
        }),
        help_text="Upload a profile picture (JPG, PNG, GIF). Max size: 5MB."
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'student_id', 'profile_picture')
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Check file size (5MB limit)
            if profile_picture.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError("Profile picture file size must be under 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if profile_picture.content_type not in allowed_types:
                raise ValidationError("Please upload a valid image file (JPG, PNG, or GIF).")
        
        return profile_picture

class CustomPasswordChangeForm(PasswordChangeForm):
    """Enhanced password change form with proper validations"""
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            # Check password strength - only length requirement
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
        
        return password 