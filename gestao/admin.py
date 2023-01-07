from django.contrib import admin
from gestao.models import perfilUsuarioModel
from gestao.forms import perfilForm
# Register your models here.
class perfilUsuarioAdmin(admin.ModelAdmin):
    form = perfilForm
admin.site.register(perfilUsuarioModel, perfilUsuarioAdmin)