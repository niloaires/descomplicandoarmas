from django import forms
from django.forms import TextInput
from django.forms.models import formset_factory
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from servicos.models import *
import decimal
class servicoForm(forms.ModelForm):
    incluirServico = models.BooleanField(default=True, verbose_name='Incluir serviço')
    nome=forms.CharField(label="Nome do Serviço", widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Serviço contratado"}))
    descricao=forms.CharField(label="Descrição", required=False, widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Descrição"}))
    sistemaVinculado=forms.CharField(label="Sistema Vinculado", widget=forms.Select(choices=opcaoSistema, attrs={"class":"form-control form-select select2"}))
    class Meta:
        model = servicosModel
        fields = ['nome', 'sistemaVinculado', 'descricao']
class cobrancaForm(forms.ModelForm):
    valorPago = forms.DecimalField(label="Valor pago", required=True, min_value=0.0,
                               widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = pagamentosServico
        fields = ['valorPago', 'formaPagamento', 'dataPagamento']
    def __init__(self, *args, **kwargs):
        #servico_id = kwargs.pop('servico_id', None)
        super(cobrancaForm, self).__init__(*args, **kwargs)

        #self.fields['servico'].initial = servico_id

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class servicoRegistroCRForm(forms.ModelForm):
    valor = forms.DecimalField(label="Valor do serviço",initial=decimal.Decimal(2000), required=True, min_value=0.0,
                               widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))

    class Meta:
        model = registroCR
        fields = ['cliente', 'clube']

    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(servicoRegistroCRForm, self).__init__(*args, **kwargs)
        if cliente_id:
            if cliente_id:
                self.fields['cliente'].initial = cliente_id
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class servicoTransferenciaSigmaSigma(forms.ModelForm):
    valor = forms.DecimalField(label="Valor do serviço", initial=decimal.Decimal(603), required=True, min_value=0.0,
                                       widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = transferenciaSigmaSigma
        fields = ['responsavel', 'alienante', 'adquirente', 'arma', 'local', 'valor']

    def __init__(self, *args, **kwargs):
        #cliente_id = kwargs.pop('cliente_id', None)
        super(servicoTransferenciaSigmaSigma, self).__init__(*args, **kwargs)
        #if cliente_id:
          #  self.fields['responsavel'].queyset=clienteModel.objects.filter(id=cliente_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        adquirente = cleaned_data.get("adquirente")
        alienante = cleaned_data.get("alienante")
        responsavel = cleaned_data.get("responsavel")
        arma = cleaned_data.get("arma")
        if alienante != responsavel and adquirente != responsavel:
            raise ValidationError(
                        "O responsável pelo serviço deve ser o alienante ou adquirente"
                    )
class formTransferenciaSinarmSigma(forms.ModelForm):
    valor = forms.DecimalField(label="Valor do serviço", initial=decimal.Decimal(603), required=True, min_value=0.0,
                                       widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = transferenciaSinarmSigma
        fields = ['responsavel', 'alienante', 'adquirente', 'arma', 'local', 'valor']

    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(formTransferenciaSinarmSigma, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['responsavel'].queyset=clienteModel.objects.filter(id=cliente_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class servicoEmissaoGTForm(forms.ModelForm):
    valor = forms.DecimalField(label="Valor do serviço", required=True, min_value=0.0,
                               widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = emissaoGuiaTrafego
        fields= ['cliente', 'arma', 'municoesLote', 'municoes', 'municoesQuantidade', 'valor']

    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(servicoEmissaoGTForm, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['cliente'].initial=cliente_id
            self.fields['arma'].queryset=armasClientes.objects.filter(cliente_id=cliente_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class armaseAcessoriosForm(forms.ModelForm):
    class Meta:
        model = armaseAcessorios
        fields = ['tipo', 'calibre', 'marcaModelo', 'quantidade']
    def __init__(self, *args, **kwargs):


        super(armaseAcessoriosForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
formSetArmaseAcessorios=formset_factory(armaseAcessoriosForm, extra=1, can_delete=True, validate_min=1)
class servicoAquisicaoPCEForm(forms.ModelForm):
    class Meta:
        model = aquisicaoPCE
        fields = ['cliente', 'finalidade', 'fornecedor', 'cR', 'anexos', 'dadosTecnicos', 'outrasInformacoes', 'local']
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(servicoAquisicaoPCEForm, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['cliente'].initial = cliente_id
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class apostimanetosCRForm(forms.ModelForm):
    valor = forms.DecimalField(label="Valor", required=True, min_value=0.0, initial=225.0,
                                   widget=forms.NumberInput(attrs={"class": "form-control show-tick"}))
    class Meta:
        model = apostilamentosExercito
        fields=['cliente', 'rM', 'objeto', 'atividade', 'apostilamento', 'outrasInformacoes', 'valor']
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(apostimanetosCRForm, self).__init__(*args, **kwargs)
        if cliente_id:
            #cliente=clienteModel.objects.get(pk=cliente_id)
            self.fields['cliente'].initial=cliente_id
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class FormDocsExigidos(forms.Form):
    def __init__(self, *args, **kwargs):
        servico_id = kwargs.pop('servico_id', None)
        super(FormDocsExigidos, self).__init__(*args, **kwargs)
        if servico_id:
            lista_pendencias=cumprimentoExigenciasModel.objects.filter(cumprida=False, servico_id=servico_id)
            for item in lista_pendencias:
                id=str(item.exigencia.pk)
                a=forms.FileField(required=True, label=item.exigencia.descricao, widget=forms.FileInput)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class servicosSisgCorpForm(forms.ModelForm):

    valor = forms.DecimalField(label="Valor do serviço", required=True, min_value=0.0,
                               widget=forms.NumberInput(attrs={"class": "how-tick", 'placeholder': '100,00'}))
    observacoes = forms.CharField(label="Observações a cerca do processo", required=False,
                                  widget=forms.Textarea(attrs={'rows': 2}))
    dataInicio = forms.CharField(required=True, label='Data de início no SISGCORP',
                                 widget=forms.DateInput(attrs={'class': 'data_mask'}))
    def __init__(self, *args, **kwargs):
        cliente_id= kwargs.pop('cliente_id', None)
        super(servicosSisgCorpForm, self).__init__(*args, **kwargs)
        if cliente_id:
            self.fields['pce'].queryset = armasClientes.objects.filter(cliente_id=cliente_id)
            self.fields['cliente'].queryset = clienteModel.objects.filter(pk=cliente_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dataInicio'].widget = TextInput(attrs={
            'class': 'form-control data_mask',
            'placeholder': 'Informe a data de entrada do requerimento no SISGCORP'})

    class Meta:
        model = servicosSisgcorpModel
        exclude = ['servico', 'ativo', 'dataRegistro']
    def clean_dataInicio(self):
        data_original=self.cleaned_data['dataInicio']
        data_formatada=datetime.datetime.strptime(data_original, "%d/%m/%Y")
        return data_formatada
    def clean_gru(self):
        gru_formatada=''.join(e for e in self.cleaned_data['gru'] if e.isalnum())
        return gru_formatada
class formMovimentacoes(forms.ModelForm):
    class Meta:
        model= movimentacoesServico
        fields =['statusServico', 'dataMovimentacao']

    def __init__(self, *args, **kwargs):
        super(formMovimentacoes, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
class requerimentosFisicosSinarmForm(forms.ModelForm):
    especificacoes=forms.CharField(required=False, label='Outras solicitações', help_text='Somente quando nenhuma das opções do campo objetivo atender a necessidade')
    class Meta:
        model = requerimentosFisicosSinarm
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(requerimentosFisicosSinarmForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_arma(self):
        cliente = self.cleaned_data['cliente']
        arma = self.cleaned_data['arma']
        if arma.cliente != cliente:
            raise ValidationError(
                "A arma escolhida não está em nome do cliente {}".format(cliente))
        elif arma.sistemaVinculado != 'SINARM':
            raise ValidationError(
                "A arma {} escolhida não está vinculada ao SINARM".format(arma))

        else:
           return arma
class apostimanetoExercitoForm(forms.ModelForm):
    class Meta:
        model = apostilamentosExercito
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super(apostimanetoExercitoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        #self.fields['anexos'].widget.attrs['rows']=1

formSetitensApostilamentoExercitoForm=inlineformset_factory(apostilamentosExercito, itensRequerimentoApostilamento, form=apostimanetoExercitoForm, exclude=['apostilamento'], extra=1)

class formRequerimentoRenovaCaoCRAFSIGMA(forms.ModelForm):
    class Meta:
        model = renovacaoCRAF
        fields = ['cliente', 'arma', 'localRequerimento']

    def __init__(self, *args, **kwargs):
        super(formRequerimentoRenovaCaoCRAFSIGMA, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    def clean_armas(self):
        arma = self.cleaned_data['arma']
        cliente = self.cleaned_data['cliente']

        if arma.cliente != cliente:
            raise ValidationError(
                "A arma {} escolhida não é de propriedade do cliente {}".format(item, cliente))
        else:
            return arma

class formTermoDoacao(forms.ModelForm):
    class Meta:
        model = termoDoacaoModel
        exclude = ['dataRegistro']

    def __init__(self, *args, **kwargs):
        super(formTermoDoacao, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    def clean_arma(self):
        arma = self.cleaned_data['arma']
        doador = self.cleaned_data['doador']

        if arma.cliente != doador:
            raise ValidationError(
                "A arma {} escolhida não é de propriedade do cliente {}".format(arma, doador))
        else:
            return arma