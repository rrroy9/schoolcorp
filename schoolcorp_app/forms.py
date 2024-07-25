from django import forms
from .models import Comment

class OTPRequestForm(forms.Form):
    email = forms.EmailField()

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6)

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Post your comment', 'rows': 3}),
        }    