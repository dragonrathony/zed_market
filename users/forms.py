from django import forms


class ProfileForm(forms.Form):
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    profile_image = forms.ImageField()
    user_name = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=100)
