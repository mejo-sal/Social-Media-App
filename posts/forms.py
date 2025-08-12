from django import forms
from .models import Post, Comment


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


class CommentCreateForm(forms.ModelForm):
    """Form for creating comments on posts"""
    
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...',
                'maxlength': '500'
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return content.strip()
