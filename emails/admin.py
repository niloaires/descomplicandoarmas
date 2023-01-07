from django.contrib import admin
from emails.models import *
# Register your models here.
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ['email', 'password']
admin.site.register(virtual_users, UsuariosAdmin)
admin.site.register(virtual_domains)

admin.site.register(virtual_aliases)