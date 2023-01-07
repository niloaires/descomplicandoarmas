from rest_framework import serializers
from processos.models import novosProcessosModel, modelosProcessosModel

class modeloProcessosSerializer(serializers.ModelSerializer):
    class Meta:
        model = modelosProcessosModel
        fields = '__all__'


class processosModelSerializer(serializers.ModelSerializer):
    modelo=modeloProcessosSerializer(read_only=True)
    percentual=serializers.SerializerMethodField()
    class Meta:
        model = novosProcessosModel
        fields = "__all__"

    def get_percentual(self, obj):
        nRequisitos=obj.modelo.requisitos.all().count()
        natendidos = obj.processosrequisitos_set.filter(atendido=True).count()
        total = (natendidos / nRequisitos) * 100
        return int(total)
