from django import forms
from django.core.exceptions import ValidationError
from pycpfcnpj import cpfcnpj
from declaracoes.models import *

class declaracaoGuardaAcervoForm(forms.ModelForm):
    class Meta:
        model = declaracaoGuardaAcervo
        fields = ['cliente', 'endereco', 'local']


    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(declaracaoGuardaAcervoForm, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['cliente'].queyset=clienteModel.objects.get(id=cliente_id)
            #self.fields['enderecoClienteModel'].queyset = enderecoClienteModel.objects.filter(cliente_id=cliente_id)
        else:
            cliente_id = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    """
        def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get("cliente")
        endereco = cleaned_data.get("enderecoClienteModel")
        qs_endereco=enderecoClienteModel.objects.get(pk=endereco)
        qs_cliente=clienteModel.objects.get(pk=cliente)
        qs_endereco=enderecoClienteModel.objects.filter(cliente=qs_cliente)
        if qs_endereco is None:
            raise ValidationError(
                        "O endereço não corresponde a um endereço válido ou vinculado ao cliente {}".format(qs_cliente.nome)
                    )
    """
class declaracoesDiversasForm(forms.ModelForm):
    texto = forms.CharField(label="Texto da declaração", required=False, widget=forms.Textarea(attrs={
        "class": ""}))
    class Meta:
        model = declaracoesDiversas
        fields = ['destinatario', 'titulo', 'local']
    def __init__(self, *args, **kwargs):
        super(declaracoesDiversasForm, self).__init__(*args ,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['texto'].widget.attrs['id'] = 'editordeTexto'
        self.fields['texto'].widget.attrs['class'] = ''

class declaracoesResidenciaDiversaForm(forms.ModelForm):
    class Meta:
        model = declarcoesResidencia
        fields = ['nomeDeclarante', 'rG', 'cpf', 'logradouro', 'estadoMunicipio', 'cep']
    def __init__(self, *args, **kwargs):
        super(declaracoesResidenciaDiversaForm, self).__init__(*args ,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_cpf(self):
        cpf=self.cleaned_data['cpf']
        validador=cpfcnpj.validate(cpf)
        if validador is False:
            raise ValidationError("O cpf informado não é válido")
        else:
            return cpf