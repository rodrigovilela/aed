from django import forms


class BuscarNoticiaForm(forms.Form):
    termo = forms.CharField(label='termo', max_length=500)