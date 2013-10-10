from django import forms
from ..models import UserProfile, User


class UserProfileForm(forms.ModelForm):
    """
    Form for creating and editing user profiles.
    """
    def __init__(self, *args, **kwargs):
        """
        Add fields for the related user model.
        """
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField()
        self.fields['first_name'] = forms.CharField()
        self.fields['last_name'] = forms.CharField()
        self.fields['email'] = forms.EmailField()
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput())
        self.fields['confirm_password'] = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        """
        Make sure the username hasn't been used previously.
        """
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if 0 != len(users):
            raise forms.ValidationError("That username is taken.")
        return username

    def clean(self):
        """
        Make sure the password confirmation matches the password.
        """
        cleaned_data = super(UserProfileForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("The passwords did not match.")
        return cleaned_data

    class Meta:
        """
        Meta options for the UserProfileForm.
        """
        model = UserProfile
        exclude = ['user']