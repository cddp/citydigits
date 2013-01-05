from django import forms
from django.contrib import admin

from lottery.models import *

#class EntryAdminForm(forms.ModelForm):
    #tags = forms.CharField(required=False)
    #class Meta:
        #model = Entry

admin.site.register(Location)
admin.site.register(Retailer)
admin.site.register(SalesWeek)
admin.site.register(Win)
admin.site.register(Interview)
admin.site.register(Photo)
admin.site.register(Borough)
admin.site.register(Neighborhood)
admin.site.register(BlockGroup)




