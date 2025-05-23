from django import forms
from .models import comicbooks

class ComicBookForm(forms.ModelForm):
    class Meta:
        model = comicbooks
        fields = '__all__'
