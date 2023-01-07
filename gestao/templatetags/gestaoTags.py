import re
from django.urls import reverse, NoReverseMatch
from django import template
from django.db.models import Case, When, Value, Sum, Count, IntegerField
import datetime
from processos.models import pendenciasModels
from financeiro.models import registrosFinanceiroModel
from processos.models import novosProcessosModel, processosRequisitos
register = template.Library()

@register.simple_tag(takes_context=True)
def ativo(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
@register.simple_tag
def checar_pendencias():
    queryset=novosProcessosModel.objects.\
        annotate(pendencias=Count(Case(When(processosrequisitos__atendido=False, then=1), output_field=IntegerField()))).\
        filter(concluido=False, pendencias__gt=1 ).order_by('-nivelPrioridade', 'ultimaMovimentacao')
    return queryset

@register.simple_tag
def checar_pendencias_financeiras():
    qs=registrosFinanceiroModel.objects.filter(ativo=True, efetivado=False).order_by('-dataPrevista')
    return qs

@register.simple_tag
def checar_processos():
    hoje=datetime.datetime.now()
    quinzeDiasAntes=hoje-datetime.timedelta(days=15)
    quinzeDiasDepois=hoje+datetime.timedelta(days=45)
    qs=novosProcessosModel.objects.annotate(tag=Case(When(dataPrevistaDeferimento__lte=hoje, then=Value('danger')),
                                                       When(dataPrevistaDeferimento__gt=hoje, then=Value('success')))).\
        filter(concluido=False, dataPrevistaDeferimento__range=[quinzeDiasAntes, quinzeDiasDepois]).order_by('dataPrevistaDeferimento')
    return qs