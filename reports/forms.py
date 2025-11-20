"""
Forms for reports app
"""

from django import forms
from django.core.exceptions import ValidationError


class ReportForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Describe your report here...',
            'class': 'form-control'
        }),
        label='Report Description',
        required=True,
        max_length=5000,
        min_length=10,
        help_text='Please provide at least 10 characters'
    )
    
    category = forms.ChoiceField(
        choices=[
            ('', '--- Select Category (Optional) ---'),
            ('safety', 'Safety Concern'),
            ('infrastructure', 'Infrastructure Issue'),
            ('environmental', 'Environmental Issue'),
            ('misconduct', 'Misconduct Report'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your name (Optional)',
            'class': 'form-control'
        }),
        label='Name',
        required=False,
        max_length=100,
        help_text='Optional - only if you want to be contacted'
    )
    
    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Location (Optional)',
            'class': 'form-control'
        }),
        label='Location',
        required=False,
        max_length=255
    )
    
    image = forms.ImageField(
        label='Upload Image (Optional)',
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        })
    )
    
    def clean_image(self):
        """Validate image file size and type"""
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB max)
            if image.size > 5242880:
                raise ValidationError('Image file size must be under 5MB')
            
            # Check file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in valid_types:
                raise ValidationError('Only JPEG, PNG, GIF, and WebP images are allowed')
        
        return image
    
    def clean_description(self):
        """Validate description content"""
        description = self.cleaned_data.get('description')
        if description:
            # Strip whitespace
            description = description.strip()
            
            # Check minimum length after stripping
            if len(description) < 10:
                raise ValidationError('Description must be at least 10 characters long')
        
        return description
