import requests

class metaData(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    def process_template_response(request, response):
        url='https://descomplicandoarmas.com.br/api/financeiro/despesas_pendentes/'
        cabecalho ={'User-Agent':''}
        parametros={}
        requisicao = requests.get(url, params=parametros, headers=cabecalho)
        despesas=requisicao.json()
        request.session['pendencias'] = despesas.count()