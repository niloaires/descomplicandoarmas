from rest_framework import viewsets
from rest_framework.response import Response
from servicos.api.serializers import *
from rest_framework.decorators import action
from servicos.models import *
class servicosViewSets(viewsets.ModelViewSet):
    queryset = servicosModel.objects.all()
    serializer_class = servicosSerializer
    @action(detail=False,  name='Últimos serviços')
    def ultimos(self, request):

        ultimos_servicos=servicosModel.objects.filter(servicoAtivo=True).order_by('-dataRegistro')
        page=self.paginate_queryset(ultimos_servicos)
        if page is not None:
            serializer=self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ultimos_servicos, many=True)
        return Response(serializer.data)