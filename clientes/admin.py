from django.contrib import admin
from clientes.models import *
# Register your models here.
@admin.action(description='Definir cliente como finalizado')
def concluirCliente(modeladmin, request, queryset):
    queryset.update(finalizado=True)

class clientesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'cpf', 'finalizado']
    ordering = ['finalizado', 'nome']
    actions = [concluirCliente]
admin.site.register(clienteModel, clientesAdmin)
admin.site.register(clienteCurso)
