from django import forms
from .models import User, ArtPost


class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone']
        widgets = {
            'password': forms.PasswordInput(),  # Use PasswordInput widget for the password field
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dictionary of field names and corresponding Tailwind CSS classes
        field_classes = {
            'username': 'mt-1 px-4 py-2 w-full border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
            'email': 'mt-1 px-4 py-2 w-full border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
            'password': 'mt-1 px-4 py-2 w-full border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
            'phone': 'mt-1 px-4 py-2 w-full border-gray-300 rounded-xl focus:outline-none focus:border-blue-500',
        }

        # Update attributes of each field's widget
        for field_name, css_classes in field_classes.items():
            self.fields[field_name].widget.attrs.update({
                'class': css_classes,
                'placeholder': field_name.capitalize(),  # Set placeholder to field name
                'required': True,  # Set other attributes if needed
            })


class find_ur_account(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone']


class loginn(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class modify_credentialsform(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_username = forms.CharField(label='New Username', max_length=100)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password == current_password:
            raise forms.ValidationError("New password should be different from the current password.")

        if new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match.")


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)


class DeleteAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ArtPostForm(forms.ModelForm):
    class Meta:
        model = ArtPost
        fields = ('image', 'title', 'category', 'type', 'description', 'price')
