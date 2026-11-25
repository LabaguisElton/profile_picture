from django import forms
from .models import PageProfile, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': "What's on your mind?",
                'maxlength': 500,
            }),
        }


class ProfilePictureForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'accept': 'image/*',
            'id': 'id_profile_picture_image',
        }),
    )

    class Meta:
        model = PageProfile
        fields = ['image']