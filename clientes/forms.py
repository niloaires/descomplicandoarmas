from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from clientes.models import *
from pycpfcnpj import cpfcnpj
import datetime
from financeiro.models import formaPagamentoChoice
from processos.models import SISTEMA_OPCOES
class clientePesquisarForm(forms.Form):
    nome = forms.CharField(label="Nome do cliente",
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome ou parte do nome"}))

class clienteForm(forms.ModelForm):
    nome = forms.CharField(label="Nome do cliente", required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo"}))
    nomeMae = forms.CharField(label="Nome da mãe", required=False,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome da mãe"}))
    nomePai = forms.CharField(label="Nome do pai", required=False,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome do pai"}))

    email = forms.CharField(label="Endereço de e-mail", required=True,
                           widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}))
    naturalidade = forms.CharField(label="Naturalidade",
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Naturalidade"}))
    ocupacao = forms.CharField(label="Ocupação", required=False,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ocupação"}))
    cpf = forms.CharField(label="CPF", required=False,
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "CPF"}))
    cR = forms.CharField(label="CR", required=False,
                          widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "CR Exército Brasileiro"}))
    tituloEleitor = forms.CharField(label="Título de eleitor", required=False,
                          widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Título de eleitor"}))
    telefone = forms.CharField(label="Número de telefone", required=True,
                          widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de telefone"}))
    nascimento = forms.CharField(localize=True, label="Data do nascimento", required=True,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control", "placeholder": "Data de nascimento", "autocomplete":"off"}))
    registroGeral = forms.CharField(label="Nº Registro Geral",required=False,
                                 widget=forms.TextInput(
                                     attrs={"class": "form-control", "placeholder": "Registro Geral"}))
    senhaAcessoGov = forms.CharField(label="Senha de acesso do acesso.gov", required=False,
                                    widget=forms.TextInput(
                                        attrs={"class": "form-control", "placeholder": "Senha de acesso do acesso.gov"}))
    genero = forms.CharField(label="Gênero", widget=forms.Select(choices=SEXO_CHOICES, attrs={
        "class": "form-control form-select select2"}))
    estadoCivil = forms.CharField(label="Estado civil", widget=forms.Select(choices=ESTADOCIVIL_CHOICES, attrs={
        "class": "form-control form-select select2", "placeholder":"Estado civil"}))
    escolaridade = forms.CharField(label="Nível de formação", widget=forms.Select(choices=ESCOLARIDADE_CHOICES, attrs={
        "class": "form-control form-select select2", "placeholder": "Escolaridade"}))
    fotoPerfil=forms.FileField(label='Foto do perfil', required=False, widget=forms.FileInput())
    #confirmar = forms.BooleanField(required=True, label='Confirmar registro ou alteração', widget=forms.CheckboxInput(attrs={'class': 'chk-col-green'}))
    class Meta:
        model = clienteModel
        fields = ('nome','nomeMae', 'nomePai', 'genero', 'cpf', 'registroGeral', 'naturalidade', 'escolaridade',     'nascimento', 'estadoCivil',
                  'tituloEleitor', 'cR', 'ocupacao', 'telefone', 'email', 'senhaAcessoGov', 'fotoPerfil')
    def __init__(self, *args, **kwargs):
        super(clienteForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['nascimento'].widget.attrs['data-mask'] = '00/00/0000'

    def clean_cpf(self):
        cpf=self.cleaned_data['cpf']
        validador=cpfcnpj.validate(cpf)
        if validador is False:
            raise ValidationError("O cpf informado não é válido")
        else:
            return cpf
    def clean_nascimento(self):
        data_nascimento=datetime.datetime.strptime(self.cleaned_data['nascimento'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if data_nascimento is None:
            raise ValidationError("Erro na data de nascimento")
        else:
            return data_nascimento
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if len(telefone)!=11:
            raise ValidationError("O número de telefone deve possuir 11 dígitos. Ex 989...")
        elif not telefone.isdecimal():
            raise ValidationError("O telefone deve possuir apenas números")
        else:
            return telefone






    def clean(self):
        cleaned_data = super().clean()
        dataEfetivacao = cleaned_data.get("dataEfetivacao")
        efetivado = cleaned_data.get("efetivado")
        dataPrevista = cleaned_data.get("dataPrevista")
        if efetivado is True and dataEfetivacao is False:
            raise ValidationError("Se o pagamento foi efetuado, é necessário informar a data!")
        if dataPrevista and dataEfetivacao is not False:
            efetivacao=datetime.datetime.strptime(self.cleaned_data['dataEfetivacao'], "%d/%m/%Y").strftime("%Y-%m-%d")
            previsao=datetime.datetime.strptime(self.cleaned_data['dataPrevista'], "%d/%m/%Y").strftime("%Y-%m-%d")
            if efetivacao < previsao:
                raise ValidationError("A data de pagamento não pode ser anterior a data de previsão")