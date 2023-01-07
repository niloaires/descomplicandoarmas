from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from financeiro.api.serializers import *

class registrosViewSets(viewsets.ModelViewSet):
    queryset = registrosFinanceiroModel.objects.filter(ativo=True)
    serializer_class = registroFinanceiroSerializer

    @action(detail=False, methods=['GET'], name='Movimentações Pendentes')
    def movimentacoes_pendentes(self, request):
        object_list = registrosFinanceiroModel.objects.filter(ativo=True, efetivado=False)
        serializer = self.get_serializer(object_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], name='Rebebimentos Pendentes')
    def recebimentos_pendentes(self, request):
        object_list=registrosFinanceiroModel.objects.filter(ativo=True, valor__gt=0, efetivado=False)
        serializer = self.get_serializer(object_list, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], name='Despesas Pendentes')
    def despesas_pendentes(self, request):
        object_list = registrosFinanceiroModel.objects.filter(ativo=True, valor__lt=0, efetivado=False)
        serializer = self.get_serializer(object_list, many=True)
        return Response(serializer.data)



