from django import forms
from django.forms.models import formset_factory
from documentos.models import arquivosModel
from clientes.models import clienteModel
class arquivosForm(forms.ModelForm):
    arquivo=forms.FileField(label='Arquivo', required=True, widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = arquivosModel
        fields = ['arquivo', 'nome', 'tipoArquivo', 'validade']
    def __init__(self, *args, **kwargs):

        super(arquivosForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['validade'].widget.attrs['class'] = 'form-control fc-datepicker'

arquivosFormSet=formset_factory(form=arquivosForm, extra=0, validate_min=1, min_num=1)