from rest_framework import serializers
from financeiro.models import registrosFinanceiroModel

class registroFinanceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = registrosFinanceiroModel
        fields = '__all__'