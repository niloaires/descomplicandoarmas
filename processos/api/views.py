from rest_framework import generics, permissions
from processos.api.serializers import processosModelSerializer
from processos.models import novosProcessosModel


class processosViewSet(generics.ListAPIView):
    serializer_class = processosModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = novosProcessosModel.objects.filter(concluido=False).order_by('-ultimaMovimentacao')[:5]
