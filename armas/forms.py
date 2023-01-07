from django import forms
from armas.models import *
from clientes.models import clienteModel
class armasForm(forms.ModelForm):
    mudancaPropriedade=forms.BooleanField(label='Em mudança de propriedade', required=False, widget=forms.CheckboxInput(attrs={'class':'form-control', 'value':True}))
    class Meta:
        model = armasClientes
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(armasForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dataRegistro'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['mudancaPropriedade'].widget.attrs['class'] = 'custom-control-input'