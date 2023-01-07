from servicos.models import *
from documentos.models import arquivosModel
from enderecos.models import enderecoClienteModel
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS




    # Criando resposta HTTP
    # response = HttpResponse(resultado, content_type='application/pdf;')
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="DECLARACOES-{cliente}.pdf"'.format(cliente=cliente.nome.upper())
    # return response