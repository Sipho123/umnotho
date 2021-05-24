from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('business_name','headline','CEO','contact_person','first_name','last_name','email','cell','land_line','industry','business_type','country','province', 'city','surburb_township','code','user','avatar','bio',)
       































