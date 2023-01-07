from django.contrib import admin
from processos.models import *
# Register your models here.
admin.site.register(ProcessosModel)
admin.site.register(historicoProcessosModel)
admin.site.register(pendenciasModels)
admin.site.register(historicoProcessos)
admin.site.register(requisitosProcessosModel)
admin.site.register(modelosProcessosModel)

class ProcessosAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'requisitosPendentes']
admin.site.register(novosProcessosModel, ProcessosAdmin)
class RequisitosProcessosAdmin(admin.ModelAdmin):
    list_display = ['id', 'requisito', 'atendido']
admin.site.register(processosRequisitos, RequisitosProcessosAdmin)