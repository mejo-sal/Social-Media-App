from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    """Form for creating new posts"""
    
    class Meta:
        model = Post
        fields = ('content', 'image', 'privacy')
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "What's on your mind?",
                'style': 'border: none; resize: none;'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file too large. Please select an image smaller than 10MB.")
            
            # Check file type
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("Please upload a valid image file.")
        
        return image
