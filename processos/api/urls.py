from django.urls import path
from processos.api.views import *

app_name='api-processos'
urlpatterns=[
    path('', processosViewSet.as_view(), name='processos')
]