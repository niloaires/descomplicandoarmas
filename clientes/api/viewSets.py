from rest_framework import viewsets, generics, permissions, status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import api_view
from clientes.api.serializers import *
from clientes.models import *
"""
class clientesViewSets(viewsets.ModelViewSet):
    queryset = clienteModel.objects.all()
    serializer_class = clientesModelSerializer
"""
class clientesViewSets(generics.ListAPIView):
    serializer_class = clientesModelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = clienteModel.objects.all()
@api_view(['POST'])
def clientes_criar(request):
    if request.method=='POST':
        serializador = ClientesModelSerializerPost(data=request.data)
        if serializador.is_valid():
            serializador.save()

            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied({"message": "Método não permitido"})


@api_view(['GET'])
def clientes_list(request):
    if request.method == 'POST':
        serializador = clientesModelSerializer(data=request.data)
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data, status=status.HTTP_201_CREATED)
        return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        queryset=clienteModel.objects.all().order_by('nome')
        serializador=clientesModelSerializer(queryset, many=True)
        return Response(serializador.data)
@api_view(['GET', 'PUT'])
def cliente_detalhar(request, pk):

    try:
        object = clienteModel.objects.get(pk=pk)
    except clienteModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializador=clientesModelSerializer(object)
        return Response(serializador.data)
    elif request.method=='PUT':
        serializador=clientesModelSerializer(object, data=request.data, partial=True        )
        if serializador.is_valid():
            serializador.save()
            return Response(serializador.data)
        else:
            return Response(serializador.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        raise PermissionDenied({"message":"Método não permitido"})


class BuscaClienteView(generics.ListAPIView):
    queryset = clienteModel.objects.all()
    serializer_class = clientesModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'cpf', 'email', 'telefone']
