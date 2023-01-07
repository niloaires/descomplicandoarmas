from rest_framework import serializers
from servicos.models import *

class servicosSerializer(serializers.ModelSerializer):
    class Meta:
        model=servicosModel
        fields='__all__'