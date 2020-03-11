from django import forms

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    

class ProcessFileForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
