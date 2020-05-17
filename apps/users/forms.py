from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas não conferem")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_('Senha'),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Senha', max_length=100, min_length=8, empty_value=False,
                                widget=forms.PasswordInput(attrs={'class': 'password-field'}), required=True)
    password2 = forms.CharField(label='Confirmar senha', max_length=100, min_length=8, empty_value=False,
                                widget=forms.PasswordInput(attrs={'class': 'password-field'}), required=True)

    def clean(self):
        if self.password1 != self.password2:
            raise forms.ValidationError("Senhas não conferem", code='Different password')
