from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('email',)
    username = forms.EmailField(max_length=64,
                                help_text="The person's email address.")
    def clean_email(self):
        email = self.cleaned_data['username']
        return email

class UserAdmin(UserAdmin):
    form = UserForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)
    search_fields = ('email',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
