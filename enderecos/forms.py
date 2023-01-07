from django import forms
from django.forms.models import inlineformset_factory
from enderecos.models import enderecoClienteModel, clienteModel
from django.core.exceptions import ValidationError


class enderecoClienteForm(forms.ModelForm):
    logradouro = forms.CharField(label="Logradouro", required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Logradouro e número"}))
    estadoMunicipio = forms.CharField(label="Município e Estado", required=True,
                                 widget=forms.TextInput(
                                     attrs={"class": "form-control", "placeholder": "Município - Estado"}))
    cep = forms.CharField(label="CEP", required=True,
                                      widget=forms.TextInput(
                                          attrs={"class": "form-control", "placeholder": "CEP"}))

    class Meta:
        model = enderecoClienteModel
        fields = ['logradouro', 'estadoMunicipio', 'cep']
    def clean_cep(self):
        cep=self.cleaned_data['cep']
        if len(cep)!=8:
            raise ValidationError("O CEP deve possuir 8 dígitos")
        elif not cep.isdecimal():
            raise ValidationError("O CEP deve possuir apenas números")
        else:
            return cep
enderecosClientesFormSet=inlineformset_factory(clienteModel, enderecoClienteModel, form=enderecoClienteForm,
                                               fields=['logradouro', 'estadoMunicipio', 'cep'], extra=1, can_delete=False, validate_min=True)