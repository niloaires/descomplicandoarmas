from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from gestao.models import perfilUsuarioModel

from gestao.models import perfilUsuarioModel

class apiLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        perfil = perfilUsuarioModel.objects.get(pk=user.id)
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'username': user.username,
            'nome_completo': str("{} {}".format(user.first_name, user.last_name)),
            'foto_perfil': perfil.avatar.url
        })
