import datetime
from django import forms
from rest_framework.exceptions import ValidationError

from financeiro.models import registrosFinanceiroModel, formaPagamentoChoice

class registrosFinanceirosForm(forms.ModelForm):
    efetivado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'chk-col-red'}))
    dataPrevista = forms.CharField(label="Data Prevista", initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                   widget=forms.TextInput(attrs={'class': 'form-control fc-datepicker'}))
    dataEfetivacao = forms.CharField(required=False, initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                     label="Data da efetivação", widget=forms.TextInput(attrs={'class': 'form-control fc-datepicker'}))
    class Meta:
        model = registrosFinanceiroModel
        fields = ['cliente','descricao', 'formaPagamento', 'codigoBarra', 'valor', 'dataPrevista', 'dataEfetivacao', 'efetivado']
    def __init__(self, *args, **kwargs):
        super(registrosFinanceirosForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dataPrevista'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['dataEfetivacao'].widget.attrs['data-mask'] = '00/00/0000'

    def clean_dataPrevista(self):
        data_prevista=datetime.datetime.strptime(self.cleaned_data['dataPrevista'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data_prevista is None:
            raise ValidationError("Erro na data prevista")
        else:
            return data_prevista
    def clean_codigoBarra(self):
        codigoBarra=self.cleaned_data['codigoBarra']
        if codigoBarra is None:
            return codigoBarra
        elif registrosFinanceiroModel.objects.filter(codigoBarra=codigoBarra).exists():
            raise ValidationError("Este código de barras já foi registrado")
        else:
            return codigoBarra
class registroFinanceiroClienteForm(forms.Form):
    descricao=forms.CharField(label="Descrição do registro", required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    codigoBarra=forms.CharField(label="Código de barras", required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Informe o código de barraso se for o caso'}))
    formaPagamento = forms.CharField(label="Forma de pagamento", required=True, widget=forms.Select(choices=formaPagamentoChoice, attrs={
        "class": "form-control form-select select2"}))
    valor=forms.CharField(label="Valor contratado", required=True, widget=forms.NumberInput(attrs={'class':'form-control'}))
    valorPago = forms.CharField(label="Valor Pago", required=True,
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    dataPrevista = forms.CharField(label='Data prevista para o pagamento', required=True,
                                   initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    dataEfetivacao = forms.CharField(label="Data do pagamento", required=False,
                                     initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", "placeholder": "Data do pagamento", "autocomplete":"off"}))

    efetivado = forms.BooleanField(label='Pagamento Efetivado', required=False,
                                   widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'value': True}))

    def __init__(self, *args, **kwargs):
        super(registroFinanceiroClienteForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dataPrevista'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['dataEfetivacao'].widget.attrs['data-mask'] = '00/00/0000'
        self.fields['efetivado'].widget.attrs['class'] = 'custom-control-input'
        self.fields['efetivado'].widget.attrs['value'] = 'Efetivado'
    def clean(self):
        cleaned_data = super().clean()
        dataEfetivacao = cleaned_data.get("dataEfetivacao")
        efetivado = cleaned_data.get("efetivado")
        dataPrevista = cleaned_data.get("dataPrevista")
        if efetivado is True and dataEfetivacao is '':
            mensagem="Se o pagamento foi efetuado, é necessário informar a data!"
            self.add_error('dataEfetivacao', mensagem)
        if dataPrevista and dataEfetivacao is not '':
            efetivacao=datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
            previsao=datetime.datetime.strptime(self.cleaned_data['dataPrevista'], "%d/%m/%Y").strftime("%Y-%m-%d")
            if efetivacao < previsao:
                mensagem = "A data de pagamento não pode ser anterior a data de previsão"
                self.add_error('dataEfetivacao', mensagem)




class registrarPagamentoForm(forms.ModelForm):
    comprovante=forms.FileField(required=False, label='Comprovante de pagamento',widget=forms.FileInput())
    formaPagamento = forms.CharField(label="Forma de pagamento", required=True,
                                     widget=forms.Select(choices=formaPagamentoChoice, attrs={
                                         "class": "form-control form-select select2"}))
    dataEfetivacao = forms.CharField(label="Data do pagamento", required=True,
                                     initial=datetime.datetime.today().strftime("%d/%m/%Y"),
                                     widget=forms.TextInput(
                                         attrs={"class": "form-control", "placeholder": "Data do pagamento",
                                                "autocomplete": "off"}))
    class Meta:
        model = registrosFinanceiroModel
        fields = ['formaPagamento', 'dataEfetivacao']

    def __init__(self, *args, **kwargs):
        super(registrarPagamentoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            self.fields['dataEfetivacao'].widget.attrs['data-mask'] = '00/00/0000'
            #self.fields['efetivado'].widget.attrs['class'] = 'custom-control-input'
            #self.fields['efetivado'].widget.attrs['value'] = 'Efetivado'

    def clean_dataEfetivacao(self):
        data_efetivacao=datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data_efetivacao is None:
            raise ValidationError("Erro na data de efetivação")
        else:
            return data_efetivacao