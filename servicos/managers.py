from django.db import models

class ServicosManager(models.Manager):
    def all(self):
        return super().all().filter(servicoAtivo=True)