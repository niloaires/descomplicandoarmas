from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User,
        fields =('username', 'email',)
        read_only_fields = ('username', 'email')

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(label='Nome do usuário', write_only=True)
    password=serializers.CharField(label='Senha', write_only=True, style={'input_type':'password'})
    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Acesso negado: Houve um problema com o seu usuário  e senha.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg= "Os campos Usuário e Password são obrigatórios."
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user']=user
        return attrs

class StatesSerializer(serializers.Serializer):
    titulo=serializers.CharField()
    t=serializers.CharField()