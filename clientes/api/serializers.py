from rest_framework import serializers
from rest_framework.decorators import api_view
from clientes.models import clienteModel
from enderecos.api.serializer import enderecosSerializer
from processos.api.serializers import processosModelSerializer
from documentos.api.serializers import ArquivosSerializer

class ClientesModelSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = clienteModel
        fields = '__all__'
class clientesModelSerializer(serializers.ModelSerializer):
    armas = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='modelo'
    )
    enderecos = enderecosSerializer(many=True, read_only=True)
    processos = processosModelSerializer(many=True, read_only=True)
    arquivos = ArquivosSerializer(many=True, read_only=True)
    estadoCivil= serializers.SerializerMethodField()
    escolaridade= serializers.SerializerMethodField()
    cpf= serializers.SerializerMethodField()
    class Meta:
        model = clienteModel
        fields ='__all__'
    def get_estadoCivil(self, obj):
        return obj.get_estadoCivil_display()
    def get_escolaridade(self,obj):
        return obj.get_escolaridade_display()
    """
        def get_telefone(self, obj):
        original=str(obj.telefone)
        if original is True:
            return str("Não informado")
        else:
            return str("({ddd}) {nonodigito} {parte1}-{parte2}".
                       format(ddd=original[:2],
                              nonodigito=original[2],
                              parte1=original[3:7],
                              parte2=original[7:11]))
    """
    def get_cpf(self, obj):
        cpf=str(obj.cpf)
        return str("{parte1}.{parte2}.{parte3}-{parte4}".format(parte1=cpf[:3],
                                                                parte2=cpf[3:6],
                                                                parte3=cpf[6:9],
                                                                parte4=cpf[9:11]))
