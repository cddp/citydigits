from django import forms
from django.contrib import admin

from lottery.models import (
        UserProfile,
        Location,
        Interview,
        Photo,
        )

#class EntryAdminForm(forms.ModelForm):
    #tags = forms.CharField(required=False)
    #class Meta:
        #model = Entry

admin.site.register(UserProfile)
admin.site.register(Location)
admin.site.register(Interview)
admin.site.register(Photo)




