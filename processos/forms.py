from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from processos.models import *
from financeiro.models import formaPagamentoChoice
class iniciarProcessoForm(forms.Form):
    processo=forms.CharField(label='Identficação do processo', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    descricao=forms.CharField(label='Descrição resumida', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    descricaoHistorico = forms.CharField(label='Descrição do processo', required=True,
                               widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Processo aguardando início'}))
    protocolo=forms.CharField(label='Protocolo', required=False, widget=forms.TextInput(attrs={'class':'form-control', 'rows':4}))
    sistemaVinculado=forms.CharField(label='Sistema Vinculado', required=True, widget=forms.Select(choices=SISTEMA_OPCOES, attrs={'class':'form-control'}))
    registroFinanceiro = forms.BooleanField(label='Registrar movimentação financeira', required=False,
                                   widget=forms.CheckboxInput(attrs={'id': 'registroFinanceiro', 'class': 'custom-control-input', 'value': True}))
    valor=forms.DecimalField(label='Valor pactuado', initial=0, required=False, widget=forms.NumberInput(attrs={'id': 'idValor', 'class':'form-control'}))
    valorPago=forms.DecimalField(label='Valor pago', initial=0, required=False, widget=forms.NumberInput(attrs={'id': 'idValorPago', 'class':'form-control'}))
    formaPagamento=forms.CharField(label='Forma de pagamento', required=False, widget=forms.Select(choices=formaPagamentoChoice,
                                                                                                   attrs={'id': 'idFormaPagamento', 'class':'form-control form-select select2'}))
    dataPrevista=forms.CharField(label='Data prevista para o pagamento', initial=datetime.datetime.today().strftime("%d/%m%Y"), required=False,
                                 widget=forms.TextInput(attrs={'id': 'idDataPrevista', 'class':'form-control', "placeholder": "Data prevista", "autocomplete":"off"}))
    efetivado=forms.BooleanField(label='Pagamento Efetivado', required=False,
                                 widget=forms.CheckboxInput(attrs={'id': 'idEfetivado', 'class':'custom-control-input', 'value':True}))
    dataEfetivacao = forms.CharField(label='Data da realização do pagamento', required=False, initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                   widget=forms.TextInput(attrs={'id': 'idDataEfetivacao', 'class': 'form-control', "placeholder": "Data do pagamento", "autocomplete":"off"}))

    def __init__(self, *args, **kwargs):
        super(iniciarProcessoForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dataPrevista'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['dataEfetivacao'].widget.attrs['data-mask'] = '00/00/0000'
        #self.fields['registroFinanceiro'].widget.attrs['checked'] = 'checked'
        self.fields['registroFinanceiro'].widget.attrs['class'] = 'custom-control-input'
        self.fields['registroFinanceiro'].widget.attrs['value'] = 'Registrar Pagamento'
        self.fields['efetivado'].widget.attrs['class'] = 'custom-control-input'
        self.fields['efetivado'].widget.attrs['checked'] = 'checked'
        self.fields['efetivado'].widget.attrs['value'] = 'Efetivado'
    def clean_dataRegistro(self):
        efetivado=self.cleaned_data['efetivado']
        data_efetivacao=datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if efetivado is True and data_efetivacao is None:
            raise ValidationError("Se o pagamento foi efetuado, é necessário informar a data!")
        else:
            return data_efetivacao
class andamentoProcessoForm(forms.ModelForm):
    class Meta:
        model = ProcessosModel
        fields = ['cliente', 'processo', 'consultaAtiva']
    def __init__(self, *args, **kwargs):

        super(andamentoProcessoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class edicaoAndamentoForm(andamentoProcessoForm):
    class Meta:
        model = ProcessosModel
        fields = ['descricao']

class historicoConsultaForm(forms.ModelForm):
    class Meta:
        model = historicoProcessosModel
        fields = ['consulta','descricao', 'textoConsulta']
    def __init__(self, *args, **kwargs):

        super(historicoConsultaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
historicoFormset = inlineformset_factory(ProcessosModel, historicoProcessosModel,
                                         form=historicoConsultaForm, extra=0, can_delete=False, min_num=1,
                                         validate_min=True)

class adicionarRegistroConsulta(forms.Form):
    descricao=forms.CharField(label='Descrição', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descreva a última movimentação processual'}))
    textoConsulta=forms.CharField(label='Histórico', help_text='Caso necessite de algum registro mais específico', required=False, widget=forms.Textarea(attrs={'rows':7, 'class':'form-control', 'placeholder':'Maiores detalhes da última movimentação processual'}))
class pendenciasForm(forms.ModelForm):
    class Meta:
        model = pendenciasModels
        fields = ['cliente', 'descricao', 'textoPendencia', 'escalaPrioridade', 'dataLimite', 'statusPendencia',]

    def __init__(self, *args, **kwargs):
        super(pendenciasForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        #self.fields['dataConclusao'].widget.attrs['class'] = 'datepicker form-control'
        self.fields['dataLimite'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['statusPendencia'].widget.attrs['class'] = 'chk-col-red'
        self.fields['textoPendencia'].widget.attrs['rows'] = 1


class novoFormProcessosModel(forms.ModelForm):
    class Meta:
        model = novosProcessosModel
        exclude=['usuario', 'concluido', 'ultimaMovimentacao', 'dataPrevistaDeferimento']

    def __init__(self, *args, **kwargs):
        super(novoFormProcessosModel, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['modelo'].label = "Tipo de processo"
        #self.fields['cliente'].queryset = clienteModel.objects.all().order_by('dataRegistro')
        self.fields['registroFinanceiro'] = forms.BooleanField(label='Registrar movimentação financeira',
                                                               required=False,
                                                               widget=forms.CheckboxInput(
                                                                   attrs={'id': 'registroFinanceiro',
                                                                          'class': 'form-check-input',
                                                                          'value': True}))
        self.fields['valor'] = forms.DecimalField(label='Valor pactuado', initial=0, required=False,
                                                  widget=forms.NumberInput(
                                                      attrs={'id': 'idValor', 'class': 'form-control'}))
        self.fields['valorPago'] = forms.DecimalField(label='Valor pago', initial=0, required=False,
                                                      widget=forms.NumberInput(
                                                          attrs={'id': 'idValorPago', 'class': 'form-control'}))
        self.fields['formaPagamento'] = forms.CharField(label='Forma de pagamento', required=False,
                                                        widget=forms.Select(choices=formaPagamentoChoice,
                                                                            attrs={'id': 'idFormaPagamento',
                                                                                   'class': 'form-control form-select select2'}))
        self.fields['dataPrevista'] = forms.CharField(label='Data prevista para o pagamento',
                                                      initial=datetime.datetime.today().strftime("%d/%m%Y"),
                                                      required=False,
                                                      widget=forms.TextInput(
                                                          attrs={'id': 'idDataPrevista', 'class': 'form-control',
                                                                 "placeholder": "Data prevista",
                                                                 "autocomplete": "off"}))
        self.fields['efetivado'] = forms.BooleanField(label='Pagamento Efetivado', required=False,
                                                      widget=forms.CheckboxInput(
                                                          attrs={'id': 'idEfetivado', 'class': 'custom-control-input',
                                                                 'value': True}))
        self.fields['dataEfetivacao'] = forms.CharField(label='Data da realização do pagamento', required=False,
                                                        initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                                        widget=forms.TextInput(
                                                            attrs={'id': 'idDataEfetivacao', 'class': 'form-control',
                                                                   "placeholder": "Data do pagamento",
                                                                   "autocomplete": "off"}))
class formProcessosModelCliente(novoFormProcessosModel):
    class Meta:
        model = novosProcessosModel
        exclude = ['cliente', 'usuario', 'ultimaMovimentacao']
    def __init__(self, *args, **kwargs):
        super(formProcessosModelCliente, self).__init__(*args, **kwargs)
        self.fields['dataPrevistaDeferimento'].widget.attrs['data-mask'] = '00/00/0000'
    def clean(self):
        cleaned_data = super().clean()
        dataEfetivacao = cleaned_data.get("dataEfetivacao")
        dataPrevistaDeferimento=cleaned_data.get("dataPrevistaDeferimento")
        efetivado = cleaned_data.get("efetivado")
        dataPrevista = cleaned_data.get("dataPrevista")
        if efetivado is True and dataEfetivacao is False:
            raise ValidationError("Se o pagamento foi efetuado, é necessário informar a data!")
        if dataPrevista and dataEfetivacao is not False:
            efetivacao=datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
            previsao=datetime.datetime.strptime(self.cleaned_data['dataPrevista'], "%d/%m/%Y").strftime("%Y-%m-%d")
            if efetivacao < previsao:
                raise ValidationError("A data de pagamento não pode ser anterior a data de previsão")


class formPendenciasProcesso(forms.ModelForm):
    class Meta:
        model = processosRequisitos
        fields = ['requisito']
    def __init__(self, *args, **kwargs):
        processo = kwargs.pop('processo', None)
        super(formPendenciasProcesso, self).__init__(*args, **kwargs)
        pendencias=processosRequisitos.objects.filter(processo__id=processo)
        self.fields['requisito']=forms.ModelMultipleChoiceField(label="Requisitos", widget=forms.CheckboxSelectMultiple,
                                                           queryset=pendencias.values('requisito__titulo'), initial=pendencias, required=False)
        self.fields['requisito'].widget.attrs['class']='form-check-input'

class formDataPrevistaDeferimento(forms.Form):
    dataPrevistaDeferimento=forms.CharField(label='Data prevista para a conclusão do processo', required=True,
                                 widget=forms.TextInput(attrs={'id': 'idDataPrevista', 'class':'form-control', "placeholder": "Data provável do deferimento", "autocomplete":"off"}))
    def __init__(self, *args, **kwargs):
        super(formDataPrevistaDeferimento, self).__init__(*args, **kwargs)
        self.fields['dataPrevistaDeferimento'].widget.attrs['data-mask'] = '00/00/0000'
    def clean(self):
        cleaned_data = super().clean()
        data=cleaned_data.get('dataPrevistaDeferimento')
        if data is not None:
            dataPrevista = datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
            return dataPrevista

class formRegistrarAnotacaoProcesso(forms.Form):
    anotacao=forms.CharField(label='Registrar anotação', required=True, widget=forms.Textarea(attrs={'class':'form-control'}))