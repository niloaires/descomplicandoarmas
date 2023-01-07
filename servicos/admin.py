from django.contrib import admin
from servicos.models import *
admin.site.register(servicosModel)
admin.site.register(transferenciaSigmaSigma)
admin.site.register(emissaoGuiaTrafego)
admin.site.register(aquisicaoPCE)
admin.site.register(exigenciasModel)
admin.site.register(registroCR)
admin.site.register(cumprimentoExigenciasModel)
admin.site.register(pagamentosServico)
admin.site.register(movimentacoesServico)
admin.site.register(cursosModel)
admin.site.register(clientesCursosModel)
class ListaServicosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'vinculoSistema', 'link']

admin.site.register(listaServicos, ListaServicosAdmin)
# Register your models here.
