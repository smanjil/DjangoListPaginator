
from django import forms


class ProductForm(forms.Form):
    title = forms.CharField(label = 'Title', max_length = 100)
    desc = forms.CharField(label = 'Description', max_length = 300, help_text = 'Write a brief description')

