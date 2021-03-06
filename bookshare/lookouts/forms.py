from django import forms
from django.forms import ModelForm, TextInput
from lookouts.models import Lookout

class LookoutForm( ModelForm ):
    class Meta:
        model = Lookout
        fields = ['ISBN']
        exclude = ['owner', 'date_created']
        labels = {
            'ISBN': 'ISBN',
        }
        widgets = {
            'ISBN': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book ISBN',
            }),
        }

class DeleteLookoutForm( forms.Form ):
    lookout_id = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput()
    )
